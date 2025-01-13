import os
import comtypes.client


class EtabsConnectionService:
    def __init__(self, program_path=None):
        """
        Initialize the EtabsConnectionService.

        :param program_path: Optional path to the ETABS executable.
        """
        self.program_path = program_path
        self._etabs_object = None
        self._sap_model = None

    def connect_to_etabs(self, attach_to_instance=False, model_path=None):
        """
        Connect to ETABS, either by attaching to an existing instance or starting a new one.

        :param attach_to_instance: Whether to attach to an existing instance.
        :param model_path: Optional path to an ETABS model to open.
        :return: True if connection is successful, False otherwise.
        """
        try:
            # Create API helper object
            helper = comtypes.client.CreateObject("ETABSv1.Helper")
            helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)

            if attach_to_instance:
                # Attach to a running instance of ETABS
                self._etabs_object = helper.GetObject("CSI.ETABS.API.ETABSObject")
            else:
                # Start a new instance of ETABS
                if self.program_path:
                    self._etabs_object = helper.CreateObject(self.program_path)
                else:
                    self._etabs_object = helper.CreateObjectProgID(
                        "CSI.ETABS.API.ETABSObject"
                    )

                self._etabs_object.ApplicationStart()

            # Initialize SapModel
            self._sap_model = self._etabs_object.SapModel

            # Open model file if provided
            if model_path:
                if not os.path.exists(model_path):
                    raise FileNotFoundError(f"Model file not found: {model_path}")
                ret = self._sap_model.File.OpenFile(model_path)
                if ret != 0:
                    raise RuntimeError(f"Failed to open model file: {model_path}")

            return True
        except (OSError, comtypes.COMError) as e:
            self._show_error(f"ETABS connection error: {e}")
            return False
        except Exception as e:
            self._show_error(f"Unexpected error: {e}")
            return False

    @property
    def sap_model(self):
        """
        Retrieve the SapModel instance.

        :return: SapModel instance.
        :raises RuntimeError: If not connected to ETABS.
        """
        if self._sap_model is None:
            raise RuntimeError("Not connected to ETABS. Call connect_to_etabs() first.")
        return self._sap_model

    @property
    def etabs_object(self):
        """
        Retrieve the EtabsObject instance.
        :return: EtabsObject instance.
        :raises RuntimeError: If not connected to ETABS.
        """
        if self._etabs_object is None:
            raise RuntimeError("Not connected to ETABS. Call connect_to_etabs() first.")
        return self._etabs_object

    @staticmethod
    def _show_error(message):
        """
        Display an error message.

        :param message: Error message to display.
        """
        print(f"Error: {message}")
