import time
from dataclasses import dataclass
from pymodbus.client import ModbusTcpClient

@dataclass
class RelaisMesures:
    tension_l1_v: float
    tension_l2_v: float
    tension_l3_v: float
    courant_l1_a: float
    courant_l2_a: float
    courant_l3_a: float
    frequence_hz: float
    horodatage: float
    etat_disjoncteur: str

class SchneiderRelayDriver:

    #port modbus = 502 par défaut, mais ici 5020 pour tester sans matériel physique et éviter les conflits
    def __init__(self, ip:str, port:int=5020, mock_backend=None):
        self.ip = ip
        self.port = port
        self._mock = mock_backend
        self._client = None
        self.connecte = False
        #self.relais_mesures = RelaisMesures(0, 0, 0, 0, 0, 0, 0, time.time(), "fermé")


    def connecter(self) -> bool:
        if self._mock is not None:
            self.connecte = True
            return True

        try:
            self._client = ModbusTcpClient(self.ip, port=self.port)
            self.connecte = self._client.connect()
            return self.connecte
        except Exception as e:
            raise ConnectionError(f"Impossible de joindre {self.ip}:{self.port} -> {str(e)}")
        

    def deconnecter(self):
        if self._client:
            self._client.close()
        self.connecte = False


    def lire_mesures(self) -> RelaisMesures:
        if not self.connecte:
            raise RuntimeError("Appeler connecter() avant de lire_mesures()")
        
        if self._mock is not None:
            return self._mock.get_mesures() #permet de tester sans matériel physique
        
        #lecture modbus physique
        regs = self._client.read_holding_registers(0, 100)  # Lire 100 registres à partir de l'adresse 0
        ETATS = {0: "OUVERT", 1: "FERME", 2:"DEFAUT"}
        return RelaisMesures(
            tension_l1_v = regs.registers[0] / 10.0,
            tension_l2_v = regs.registers[2] / 10.0,
            tension_l3_v = regs.registers[4] / 10.0,
            courant_l1_a = regs.registers[6] / 10.0,
            courant_l2_a = regs.registers[8] / 10.0,
            courant_l3_a = regs.registers[10] / 10.0,
            frequence_hz = regs.registers[12] / 10.0,
            horodatage = time.time(),
            etat_disjoncteur = ETATS.get(regs.registers[99], "INCONNU")
        )
