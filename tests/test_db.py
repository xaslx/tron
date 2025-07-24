import pytest
from src.repositories.tron import BaseTronRepository


@pytest.mark.asyncio
async def test_add_to_bd(tron_repo: BaseTronRepository):

    initial_total, initial_items = await tron_repo.get_paginated_list()
    assert initial_total == 0
    assert len(initial_items) == 0


    test_address = 'TRzQ1234567890'
    await tron_repo.log(address=test_address)


    new_total, new_items = await tron_repo.get_paginated_list()
    assert new_total == 1
    assert len(new_items) == 1
    assert new_items[0].address == test_address