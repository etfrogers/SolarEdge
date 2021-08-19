import datetime

from solaredgeoptimiser import yr_client
from solaredgeoptimiser.config import config, logger, LOG_TIME_FORMAT
from solaredgeoptimiser.solar_edge_api import get_power_flow, get_battery_level, BatteryNotFoundError


def main():
    forecast = yr_client.get_forecast(config['site-location'])
    coverage = yr_client.get_cloud_cover(forecast)
    logger.info(f'Average coverage from {datetime.datetime.now().__format__(LOG_TIME_FORMAT)} '
                f'until peak time ({config["peak-time"][0]}) is {coverage}')
    get_power_flow()
    try:
        battery_charge = get_battery_level()
    except BatteryNotFoundError as err:
        logger.error(str(err) + ' - Stopping execution')
        return
    logger.info(f'Battery charge: {battery_charge}%')


if __name__ == '__main__':
    # noinspection PyBroadException
    try:
        main()
    except Exception:
        logger.exception(str(Exception))
