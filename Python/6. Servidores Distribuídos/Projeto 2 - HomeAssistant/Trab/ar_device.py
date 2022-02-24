import grpc
from concurrent import futures
import time

# import the generated classes
import ar_pb2
import ar_pb2_grpc


class ArServicer(ar_pb2_grpc.ArServicer):

    def ligarAr(self, request, context):
        response = ar_pb2.ArTemperatura()
        print(response)
        response.temperatura = request.temperatura
        return response

    def desligarAr(self, request, context):
        response = ar_pb2.ArTemperatura()
        print(response)
        response.temperatura = -1
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

ar_pb2_grpc.add_ArServicer_to_server(
    ArServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50052.')
server.add_insecure_port('[::]:50052')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
