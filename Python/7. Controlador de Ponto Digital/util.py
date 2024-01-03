from datetime import datetime, timedelta

class PontoError(Exception):
    pass

class RegistradorPonto:
    def __init__(self, carga_horaria_diaria=8):
        self.carga_horaria_diaria = carga_horaria_diaria
        self.pontos = {'entrada': None, 'saida_almoco': None, 'volta_almoco': None, 'saida': None}

    def validar_horario(self, horario):
        if not isinstance(horario, datetime):
            raise PontoError('Erro: Horário fornecido não é um objeto datetime válido.')

    def registrar_ponto(self, ponto, horario=None):
        if ponto not in self.pontos:
            raise PontoError('Erro: Ponto inválido.')

        if horario:
            self.validar_horario(horario)
            if self.pontos[ponto] and horario < self.pontos[ponto]:
                raise PontoError(f'Erro: O horário de {ponto} deve ser maior que o horário anterior.')
            self.pontos[ponto] = horario
        else:
            self.pontos[ponto] = datetime.now()
            if self.pontos[ponto] < self.pontos['entrada']:
                raise PontoError(f'Erro: O horário de {ponto} deve ser maior que o horário anterior.')
        
        print(f'Ponto de {ponto} registrado às {self.pontos[ponto].strftime("%H:%M:%S")}')

    def calcular_horas_entre_pontos(self, ponto_inicial, ponto_final):
        if ponto_inicial not in self.pontos or ponto_final not in self.pontos:
            raise PontoError('Erro: Pontos inválidos.')

        if self.pontos[ponto_inicial] is None or self.pontos[ponto_final] is None:
            raise PontoError('Erro: Registre ambos os pontos antes de calcular as horas entre eles.')

        if ponto_inicial == 'saida_almoco' and ponto_final == 'volta_almoco':
            print('Erro: Intervalo de tempo livre/almoço. Não computado como tempo de trabalho.')
            return

        if self.pontos[ponto_final] < self.pontos[ponto_inicial]:
            raise PontoError('Erro: O horário do ponto final deve ser maior que o horário do ponto inicial.')

        horas_entre_pontos = (self.pontos[ponto_final] - self.pontos[ponto_inicial]).total_seconds() / 3600
        print(f'Horas entre {ponto_inicial} e {ponto_final}: {horas_entre_pontos:.2f} horas')

        # Calculando a quantidade de horas que falta para atingir a carga horária diária
        horas_acumuladas = sum([(self.pontos[p] - self.pontos[ponto_inicial]).total_seconds() / 3600
                                for p in self.pontos if p != ponto_inicial and self.pontos[p] is not None])
        horas_faltantes = max(0, self.carga_horaria_diaria - horas_acumuladas)
        print(f'Horas faltantes para completar o dia: {horas_faltantes:.2f} horas')

    def calcular_horas_restantes(self):
        pontos_trabalhados = [self.pontos[p] for p in self.pontos if self.pontos[p] is not None
                              and p not in ['saida_almoco']]

        pontos_trabalhados_set = set(pontos_trabalhados)
        if len(pontos_trabalhados_set) < 2:
            raise PontoError('Erro: Registre pelo menos dois pontos distintos para calcular as horas restantes.')

        pontos_trabalhados_set -= {self.pontos['saida_almoco'], self.pontos['volta_almoco']}

        pontos_trabalhados = sorted(list(pontos_trabalhados_set))

        horas_trabalhadas = sum([(pontos_trabalhados[i + 1] - pontos_trabalhados[i]).total_seconds() / 3600
                                 for i in range(len(pontos_trabalhados) - 1)])
        horas_restantes = self.carga_horaria_diaria - horas_trabalhadas
        print(f'Horas restantes: {horas_restantes:.2f} horas')

        hora_estimada = datetime.now() + timedelta(hours=horas_restantes)
        print(f'Estimativa do horário para completar as 8 horas: {hora_estimada.strftime("%H:%M:%S")}')