from tests.api_workflow.mocked_api_workflow_client import MockedApiWorkflowSetup


class TestApiWorkflowDatasources(MockedApiWorkflowSetup):
    def test_get_processed_until_timestamp(self):
        self.api_workflow_client._datasources_api.reset()
        assert self.api_workflow_client.get_processed_until_timestamp() == 0

    def test_update_processed_until_timestamp(self):
        self.api_workflow_client._datasources_api.reset()
        self.api_workflow_client.update_processed_until_timestamp(10)
        assert self.api_workflow_client.get_processed_until_timestamp() == 10

    def test_download_raw_samples(self):
        self.api_workflow_client._datasources_api.reset()
        samples = self.api_workflow_client.download_raw_samples()
        num_samples = self.api_workflow_client._datasources_api._num_samples
        assert len(samples) == num_samples

    def test_download_raw_samples_no_duplicates(self):
        self.api_workflow_client._datasources_api.reset()
        samples = self.api_workflow_client.download_raw_samples()
        assert len(samples) == len(set(samples))

    def test_download_new_raw_samples_no_duplicates(self):
        self.api_workflow_client._datasources_api.reset()
        samples = self.api_workflow_client.download_new_raw_samples()
        assert len(samples) == len(set(samples))

    def test_download_new_raw_samples_not_yet_processed(self):
        self.api_workflow_client._datasources_api.reset()
        samples = self.api_workflow_client.download_raw_samples()
        num_samples = self.api_workflow_client._datasources_api._num_samples
        assert len(samples) == num_samples

    def test_download_new_raw_samples_partially_processed(self):
        self.api_workflow_client._datasources_api.reset()
        num_samples = self.api_workflow_client._datasources_api._num_samples
        n_processed = num_samples // 2
        n_remaining = num_samples - n_processed
        processed_timestamp = n_processed - 1
        self.api_workflow_client.update_processed_until_timestamp(processed_timestamp)
        samples = self.api_workflow_client.download_new_raw_samples()
        assert len(samples) == n_remaining

    def test_download_raw_samples_equal_to_download_all_raw_new_samples(self):
        self.api_workflow_client._datasources_api.reset()
        samples = self.api_workflow_client.download_raw_samples()
        new_samples = self.api_workflow_client.download_new_raw_samples()
        assert len(samples) == len(new_samples)
        assert set(samples) == set(new_samples)