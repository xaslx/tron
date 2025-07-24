from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


@pytest.mark.asyncio
async def test_get_tron_data_success(client: AsyncClient, db_session: AsyncSession):
    test_address = 'TBEp1Gndqp88SUWnS4NQH5CAMhduHgpoNY'
    
    response = await client.get(f'/api/tron?address={test_address}')
    
    assert response.status_code == 200
    data = response.json()
    assert data
    await db_session.execute(text('DELETE FROM tron_requests WHERE address = :address'), {'address': test_address})
    await db_session.commit()


@pytest.mark.asyncio
async def test_get_tron_data_fail(client: AsyncClient):
    test_address = 'test'

    response = await client.get(f'/api/tron?address={test_address}')

    assert response.status_code == 400
    assert response.json() == {'detail': 'Неверный Tron адрес'}


@pytest.mark.asyncio
async def test_get_requests_success(client: AsyncClient, sample_tron_requests):

    response = await client.get('/api/requests?skip=0&limit=10')

    assert response.status_code == 200
    data = response.json()

    assert data['total'] == 2
    assert len(data['items']) == 2
    assert data['items'][0]['address'] == sample_tron_requests[0].address
