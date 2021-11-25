from json import dumps

from loader import iis_connector, db_connector


async def get_all_offices():
    """

    :return:
    """
    units = await iis_connector.units_list()
    await db_connector.add_offices_info(dumps(units, ensure_ascii=False))
