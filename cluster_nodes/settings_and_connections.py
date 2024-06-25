"""
https://docs.couchbase.com/server/current/rest-api/rest-rebalance-overview.html
"""
from cb_server_rest_util.connection import CBRestConnection


class SettingsAndConnectionsAPI(CBRestConnection):
    def __init__(self):
        super(SettingsAndConnectionsAPI, self).__init__()

    def set_internal_settings(self, setting_name=None, setting_value=None):
        """
        GET / POST :: /internalSettings
        docs.couchbase.com/server/current/rest-api/rest-get-internal-setting.html
        """
        api = self.base_url + "/internalSettings"
        if setting_name is None:
            # GET method
            status, content, _ = self.request(api, CBRestConnection.GET)
        else:
            # POST method
            params = {setting_name: setting_value}
            status, content, _ = self.request(api, CBRestConnection.POST,
                                              params=params)
        return status, content

    def set_auto_compaction_settings(self, parallel_db_and_vc="false",
                                     db_fragment_threshold=None,
                                     view_fragment_threshold=None,
                                     db_fragment_threshold_percentage=None,
                                     view_fragment_threshold_percentage=None,
                                     allowed_time_period_from_hour=None,
                                     allowed_time_period_from_min=None,
                                     allowed_time_period_to_hour=None,
                                     allowed_time_period_to_min=None,
                                     allowed_time_period_abort=None):
        """
        POST /controller/setAutoCompaction
        docs.couchbase.com/server/current/manage/manage-settings/configure-compact-settings.html#configure-auto-compaction-with-the-rest-api
        """
        params = dict()
        api = f"{self.base_url}/controller/setAutoCompaction"

        params["parallelDBAndViewCompaction"] = parallel_db_and_vc
        # Need to verify None because the value could be = 0
        if db_fragment_threshold is not None:
            params["databaseFragmentationThreshold[size]"] = \
                db_fragment_threshold
        if view_fragment_threshold is not None:
            params[
                "viewFragmentationThreshold[size]"] = view_fragment_threshold
        if db_fragment_threshold_percentage is not None:
            params["databaseFragmentationThreshold[percentage]"] = \
                db_fragment_threshold_percentage
        if view_fragment_threshold_percentage is not None:
            params["viewFragmentationThreshold[percentage]"] = \
                view_fragment_threshold_percentage
        if allowed_time_period_from_hour is not None:
            params[
                "allowedTimePeriod[fromHour]"] = allowed_time_period_from_hour
        if allowed_time_period_from_min is not None:
            params[
                "allowedTimePeriod[fromMinute]"] = allowed_time_period_from_min
        if allowed_time_period_to_hour is not None:
            params["allowedTimePeriod[toHour]"] = allowed_time_period_to_hour
        if allowed_time_period_to_min is not None:
            params["allowedTimePeriod[toMinute]"] = allowed_time_period_to_min
        if allowed_time_period_abort is not None:
            params[
                "allowedTimePeriod[abortOutside]"] = allowed_time_period_abort

        status, content, _ = self.request(api, self.POST, params)
        return status, content

    def manage_internal_settings_max_parallel_indexers(self, value=None):
        """
        GET / POST /internalSettings/maxParallelIndexers
        https://docs.couchbase.com/server/current/rest-api/rest-get-internal-setting.html
        :param value:
        :return:
        """
        api = self.base_url + "/internalSettings/maxParallelIndexers"
        if value is None:
            # GET method
            status, response = self.request(api, CBRestConnection.GET)
        else:
            # POST method
            params = {"globalValue": value}
            status, response = self.request(api, CBRestConnection.POST,
                                            params=params)
        content = response.json if status else response.text
        return status, content

    def manage_cluster_connections(self, max_connections=None,
                                   system_connections=None, num_writer_threads=None, num_reader_threads=None,
                                   num_storage_threads=None):
        """
        POST / GET /pools/default/settings/memcached/global
        https://docs.couchbase.com/server/current/rest-api/rest-manage-cluster-connections.html
        :param max_connections:
        :param system_connections:
        :return:
        """
        api = self.base_url + "/pools/default/settings/memcached/global"
        params = dict()
        if max_connections is not None:
            params["max_connections"] = max_connections
        if system_connections is not None:
            params["system_connections"] = system_connections
        if num_reader_threads is not None:
            params["num_reader_threads"] = num_reader_threads
        if num_writer_threads is not None:
            params["num_writer_threads"] = num_writer_threads
        if num_storage_threads is not None:
            params["num_storage_threads"] = num_storage_threads
        if params:
            # POST method
            status, _, response = self.request(api, CBRestConnection.POST,
                                            params=params)
        else:
            # GET method
            status, _, response = self.request(api, CBRestConnection.GET)
        content = response.json if status else response.text
        return status, content

    def manage_alternate_address(self, alternate_addr, alternate_ports=None,
                                 delete_address=False):
        """
        GET / POST /node/controller/setupAlternateAddresses/external
        https://docs.couchbase.com/server/current/rest-api/rest-set-up-alternate-address.html
        :param alternate_addr:
        :param alternate_ports:
        :param delete_address:
        :return:
        """
        params = ''
        api = self.base_url \
            + '/node/controller/setupAlternateAddresses/external'

        method = CBRestConnection.PUT
        if delete_address:
            method = CBRestConnection.DELETE
        else:
            params = {"hostname": alternate_addr}
            if alternate_ports:
                for service, port in alternate_ports.items():
                    params_dict[service] = port

        status, response = self.request(api, method, params)
        content = response.json if status else response.text
        return status, content

    def manage_alerts(self, email_password=None, sender=None, recipients=None,
                      email_host=None, encrypt_email=None, alerts=None,
                      pop_up_alerts=None, enabled='true'):
        """
        GET / POST /settings/alerts
        https://docs.couchbase.com/server/current/rest-api/rest-cluster-email-notifications.html
        :return:
        """
        params = dict()
        """
        -d emailPass=<email-password>
        -d sender=<sender-email-address>
        -d recipients=<list-of-recipient-email-addresses>
        -d emailHost=<ip-address-or-domain-name>
        -d emailPort=<email-server-port-number>
        -d emailEncrypt=[ true | false ]
        -d alerts=<[alert-name]*>
        -d pop_up_alerts=<[alert-name]*>
        enabled=[ true | false ]"""
