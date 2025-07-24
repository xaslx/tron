from dataclasses import dataclass
from decimal import Decimal

from tronpy import Tron
from tronpy.exceptions import BadAddress
from src.repositories.tron import BaseTronRepository
from src.schemas.tron import TronInfo
from src.exceptions.tron import InvalidTronAddressException


@dataclass
class GetTronInfoUseCase:
    
    _tron_client: Tron
    _tron_repository: BaseTronRepository

    async def execute(self, address: str) -> TronInfo:

        try:
            energy: int = self._tron_client.get_energy(address=address)
            bandwidth: int = self._tron_client.get_bandwidth(addr=address)
            balance: Decimal = self._tron_client.get_account_balance(addr=address)
            result: TronInfo = TronInfo(bandwidth=bandwidth, energy=energy, balance=float(balance))
            await self._tron_repository.log(address)
            return result
        except BadAddress:
            raise InvalidTronAddressException()


        