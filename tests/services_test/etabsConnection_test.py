import unittest
from unittest.mock import patch, MagicMock
from sp_editor.services.etabsConnection_service import EtabsConnectionService


class TestEtabsConnectionService(unittest.TestCase):

    @patch("sp_editor.services.etabsConnection_service.comtypes.client.CreateObject")
    def test_connect_to_etabs_attach_to_instance_success(self, mock_create_object):
        # Mock the ETABS Helper and object
        mock_helper = MagicMock()
        mock_etabs_object = MagicMock()
        mock_helper.GetObject.return_value = mock_etabs_object
        mock_create_object.return_value.QueryInterface.return_value = mock_helper

        # Create the service
        service = EtabsConnectionService()

        # Test attaching to an existing instance
        success = service.connect_to_etabs(attach_to_instance=True)

        # Assertions
        self.assertTrue(success)
        mock_create_object.assert_called_once_with("ETABSv1.Helper")
        mock_helper.GetObject.assert_called_once_with("CSI.ETABS.API.ETABSObject")

    @patch("sp_editor.services.etabsConnection_service.comtypes.client.CreateObject")
    def test_connect_to_etabs_start_new_instance_success(self, mock_create_object):
        # Mock the ETABS Helper and object
        mock_helper = MagicMock()
        mock_etabs_object = MagicMock()
        mock_helper.CreateObjectProgID.return_value = mock_etabs_object
        mock_create_object.return_value.QueryInterface.return_value = mock_helper

        # Create the service
        service = EtabsConnectionService()

        # Test starting a new instance
        success = service.connect_to_etabs(attach_to_instance=False)

        # Assertions
        self.assertTrue(success)
        mock_create_object.assert_called_once_with("ETABSv1.Helper")
        mock_helper.CreateObjectProgID.assert_called_once_with("CSI.ETABS.API.ETABSObject")
        mock_etabs_object.ApplicationStart.assert_called_once()

    @patch("sp_editor.services.etabsConnection_service.comtypes.client.CreateObject")
    def test_connect_to_etabs_open_model_file_success(self, mock_create_object):
        # Mock the ETABS Helper and object
        mock_helper = MagicMock()
        mock_etabs_object = MagicMock()
        mock_sap_model = MagicMock()
        mock_etabs_object.SapModel = mock_sap_model
        mock_helper.CreateObjectProgID.return_value = mock_etabs_object
        mock_create_object.return_value.QueryInterface.return_value = mock_helper

        # Mock the model file opening
        mock_sap_model.File.OpenFile.return_value = 0

        # Create the service
        service = EtabsConnectionService()

        # Test starting a new instance and opening a model file
        with patch("os.path.exists", return_value=True):
            success = service.connect_to_etabs(attach_to_instance=False, model_path="example.edb")

        # Assertions
        self.assertTrue(success)
        mock_sap_model.File.OpenFile.assert_called_once_with("example.edb")

    @patch("sp_editor.services.etabsConnection_service.comtypes.client.CreateObject")
    def test_connect_to_etabs_model_file_not_found(self, mock_create_object):
        # Mock the ETABS Helper
        mock_helper = MagicMock()
        mock_create_object.return_value.QueryInterface.return_value = mock_helper

        # Create the service
        service = EtabsConnectionService()

        # Test with a non-existent model file
        with patch("os.path.exists", return_value=False):
            success = service.connect_to_etabs(attach_to_instance=False, model_path="nonexistent.edb")

        # Assertions
        self.assertFalse(success)

    @patch("sp_editor.services.etabsConnection_service.comtypes.client.CreateObject")
    def test_sap_model_property_not_connected(self, mock_create_object):
        # Create the service without connecting
        service = EtabsConnectionService()

        # Test the sap_model property without connecting
        with self.assertRaises(RuntimeError) as context:
            _ = service.sap_model

        # Assertions
        self.assertEqual(str(context.exception), "Not connected to ETABS. Call connect_to_etabs() first.")

    @patch("sp_editor.services.etabsConnection_service.comtypes.client.CreateObject")
    def test_etabs_object_property_not_connected(self, mock_create_object):
        # Create the service without connecting
        service = EtabsConnectionService()

        # Test the etabs_object property without connecting
        with self.assertRaises(RuntimeError) as context:
            _ = service.etabs_object

        # Assertions
        self.assertEqual(str(context.exception), "Not connected to ETABS. Call connect_to_etabs() first.")


if __name__ == "__main__":
    unittest.main()
