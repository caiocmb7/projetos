import sys
import cv2
import traceback
import torch

yoloVersion = 'v5'

if yoloVersion == 'v5':
    #YOLOV5 PyTorch

    torch.cuda.empty_cache()

    #veiculo
    vehicle_model = torch.hub.load('ultralytics/yolov5', 'custom', path="V5/veiculos/best_carro_antigo.pt")
    #placa
    plate_model = torch.hub.load('ultralytics/yolov5', 'custom', path="V5/placas/best_placa_antigo.pt")
    #OCR
    OCR_model = torch.hub.load('ultralytics/yolov5', 'custom', path="V5/OCR/best_OCR_novo.pt")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)

else:

    #YOLOV4 DarkNet

    #veiculo
    veiculo_weights = 'V4/V4Tiny/veiculos/yolov4-tiny-custom_final_veiculo.weights' 
    veiculo_netcfg  = 'V4/V4Tiny/veiculos/yolov4-tiny-custom_veiculo.cfg'

    veiculo_net  = cv2.dnn.readNet(veiculo_netcfg, veiculo_weights)
    vehicle_model = cv2.dnn_DetectionModel(veiculo_net)
    vehicle_model.setInputParams(size=(256,256), scale=1/255)

    #placa
    placa_weights = 'V4/V4Tiny/placas/yolov4-tiny-custom_best_placa.weights' 
    placa_netcfg  = 'V4/V4Tiny/placas/yolov4-tiny-custom_placa.cfg'

    placa_net  = cv2.dnn.readNet(placa_netcfg, placa_weights)
    plate_model = cv2.dnn_DetectionModel(placa_net)
    plate_model.setInputParams(size=(256,256), scale=1/255)
    
    #OCR
    ocr_weights = 'V4/V4Tiny/OCR/yolov4-tiny-custom_final_OCR.weights' 
    ocr_netcfg  = 'V4/V4Tiny/OCR/yolov4-tiny-custom_OCR.cfg'

    ocr_net  = cv2.dnn.readNet(ocr_netcfg, ocr_weights)
    OCR_model = cv2.dnn_DetectionModel(ocr_net)
    OCR_model.setInputParams(size=(256,256), scale=1/255)

vehicle_classes = []
with open("veiculos.names", "r") as f:
	vehicle_classes = [cname.strip() for cname in f.readlines()]

ocr_classes = []
with open("ocr-net.names", "r") as f:
	ocr_classes = [cname.strip() for cname in f.readlines()]

filters = ["carro", "moto"]

def vehicle_detect(frame):
    global yoloVersion, vehicle_model

    rets = []

    if yoloVersion == 'v5':
        res = vehicle_model(frame)

        for i in res.xyxy[0]:
            x1 = int(i[0])
            y1 = int(i[1])
            x2 = int(i[2])
            y2 = int(i[3])
            rets.append([[x1,y1,x2,y2], i[4], int(i[5])])
    else:
        c, s, b = vehicle_model.detect(frame, 0.2, 0.1)

        for(classid, score, box) in zip(c, s, b):
            x1 = int(box[0])
            y1 = int(box[1])
            x2 = int(box[0]+box[2])
            y2 = int(box[1]+box[3])
            rets.append([[x1,y1,x2,y2], score, classid[0]])
    return rets

def alpr_detect(frame):
    
    global yoloVersion, plate_model

    results = []
    try:  
        
        if frame is not None:
            rets = []

            if yoloVersion == 'v5':
                res = plate_model(frame)

                for i in res.xyxy[0]:
                    x1 = int(i[0])
                    y1 = int(i[1])
                    x2 = int(i[2])
                    y2 = int(i[3])
                    rets.append([[x1,y1,x2-x1,y2-y1], int(i[5])])
            else:

                c, s, b = plate_model.detect(frame, 0.2, 0.1)

                for(classid, score, box) in zip(c, s, b):
                    x1 = int(box[0])
                    y1 = int(box[1])
                    x2 = int(box[2])
                    y2 = int(box[3])
                    rets.append([[x1,y1,x2,y2], classid[0]])
            

            if len(rets):
                for r , c in rets:
                    x,y,w,h = r
                    x, y, w, h = max(0, x), max(0, y), max(0, w), max(0, h)
                    
                    results.append(((x,y,w,h), c))
    except:
        traceback.print_exc()
        sys.exit(1)

    return results

def ocr_detect(frame):
    global yoloVersion, OCR_model

    text_plate = None

    try:

        rets = []
        text_plate = ""
        plate_list = []

        if yoloVersion == 'v5':
            res = OCR_model(frame)
            for i in res.xyxy[0]:
                x1 = int(i[0])
                y1 = int(i[1])
                x2 = int(i[2])
                y2 = int(i[3])
                rets.append([[x1,y1,x2-x1,y2-y1], int(i[5])])

        else:
            c, s, b = OCR_model.detect(frame, 0.2, 0.1)
            for classId, score, boxL in zip(c,s,b):
                if score < 0.3:
                    continue
                rets.append([[boxL[0],boxL[1],boxL[2],boxL[3]], classId[0]])


        for boxL, classId in rets:

            if boxL[2]*boxL[3] > 700:
                continue
            stop = False
            for b in plate_list:
                if abs(boxL[0]-b[0]) < 5:
                    stop = True
                    break
            if stop:
                continue
            char = ocr_classes[classId]
            cv2.rectangle(frame, boxL, (255,0,0), 1)
            cv2.putText(frame, char, (boxL[0]+2,boxL[1]-2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            
            if len(plate_list)==0:
                plate_list.append((boxL[0],char))
            else:
                tamList = len(plate_list)
                inserido = False
                for i in range(tamList):
                    if plate_list[i][0] > boxL[0]:
                        plate_list.insert(i,(boxL[0],char))
                        inserido = True
                        break
                if not inserido:
                    plate_list.append((boxL[0],char))

        plate_list = [x2 for x1,x2 in plate_list]
        text_plate = "".join(plate_list)
               
    except:
        traceback.print_exc()
        sys.exit(1)

    return text_plate


def fixPlateOCR(lp_str, classPlate):
    if len(lp_str)==7:
        lp_str = list(lp_str)

        letters = [0,1,2] if classPlate==0 else [0,1,2,4]
        numbers = [3,4,5,6] if classPlate==0 else [3,5,6]

        for ch in letters:
            if lp_str[ch] == '0': lp_str[ch] = 'O'
            elif lp_str[ch] == '1': lp_str[ch] = 'I'
            elif lp_str[ch] == '5': lp_str[ch] = 'S'
            elif lp_str[ch] == '6': lp_str[ch] = 'G'
            elif lp_str[ch] == '7': lp_str[ch] = 'T'
            elif lp_str[ch] == '8': lp_str[ch] = 'B'

        for ch in numbers:
            if lp_str[ch] == 'B': lp_str[ch] = '8'
            elif lp_str[ch] == 'D': lp_str[ch] = '0'
            elif lp_str[ch] == 'G': lp_str[ch] = '6'
            elif lp_str[ch] == 'I': lp_str[ch] = '1'
            elif lp_str[ch] == 'O': lp_str[ch] = '0'
            elif lp_str[ch] == 'Q': lp_str[ch] = '0'
            elif lp_str[ch] == 'S': lp_str[ch] = '5'
            elif lp_str[ch] == 'T': lp_str[ch] = '7'
            elif lp_str[ch] == 'Z': lp_str[ch] = '2'
        lp_str = "".join(lp_str)
    return lp_str
