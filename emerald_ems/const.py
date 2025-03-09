from logging import Logger, getLogger
from urllib.parse import urljoin

LOGGER: Logger = getLogger(__package__)

NAME = "Emerald EMS"
DOMAIN = "emerald_ems"
ATTRIBUTION = "Data provided by http://emerald-ems.com.au"
ISSUE_URL = "https://github.com/mrbretticus/emerald-ems/issues"

# API
API_URL = "https://api.emerald-ems.com.au/api/v1/"
FLASHDATA_API_URL = "https://api.sync.flashdata.ihd.eems.app/"

# Endpoints
SIGN_IN_URL = urljoin(API_URL, "./customer/sign-in")
PROPERTY_LIST_URL = urljoin(API_URL, './customer/property/list')
PROPERTY_INFO_URL = urljoin(API_URL, './customer/property/get-info')
DEVICE_FLASHES_URL = urljoin(FLASHDATA_API_URL, './customer/device/get-by-date/flashes-data')
