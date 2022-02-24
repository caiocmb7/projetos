import grpc
from concurrent import futures
import time

# import the generated classes
import lampada_pb2
import lampada_pb2_grpc


class LampadaServicer(lampada_pb2_grpc.LampadaServicer):

    def ligarLampada(self, request, context):
        response = lampada_pb2.LampadaStatus()
        response.stauts = 500
        return response

    def desligarLampada(self, request, context):
        response = lampada_pb2.LampadaStatus()
        response.stauts = -1
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

lampada_pb2_grpc.add_LampadaServicer_to_server(
    LampadaServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
