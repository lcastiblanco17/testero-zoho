
import os
from zcrmsdk.src.com.zoho.crm.api.bulk_read import *
from zcrmsdk.src.com.zoho.crm.api.util import Choice
class BulkRead(object):
    @staticmethod
    def download_result(job_id, destination_folder):

        """
        This method is used to download the result of Bulk Read operation
        :param job_id: The unique ID of the bulk read job.
        :param destination_folder: The absolute path where downloaded file has to be stored.
        """

        """
        example
        job_id = 3409643000002461001
        """

        # Get instance of BulkReadOperations Class
        #creamos la instancia igual que en los anteriores archivos, si nos fijamos bien el patron se repite 
        bulk_read_operations = BulkReadOperations()

        # Call download_result method that takes job_id as parameter
        response = bulk_read_operations.download_result(job_id)

        if response is not None:

            # Get the status code from response
            print('Status Code: ' + str(response.get_status_code()))

            if response.get_status_code() in [204, 304]:
                print('No Content' if response.get_status_code() == 204 else 'Not Modified')
                return

            # Get object from response
            response_object = response.get_object()

            if response_object is not None:

                # Check if expected FileBodyWrapper instance is received.
                if isinstance(response_object, FileBodyWrapper):

                    # Get StreamWrapper instance from the returned FileBodyWrapper instance
                    stream_wrapper = response_object.get_file()

                    # Construct the file name by joining the destinationFolder and the name from StreamWrapper instance
                    #En esta linea definimos donde se va almacenar el dataset y ademas especificando el nombre que va a tener el archivo.
                    file_name = os.path.join(destination_folder, stream_wrapper.get_name())

                    # Open the destination file where the file needs to be written in 'wb' mode
                    #Abrimos el directorio para guardar el archivo en el formato especificado en este caso csv
                    with open(file_name, 'wb') as f:
                        # Get the stream from StreamWrapper instance
                        for chunk in stream_wrapper.get_stream():
                            f.write(chunk)

                        f.close()

                # Check if the request returned an exception
                #En caso de que no se pueda completar la descarga lanzamos esta excepcion y los detalles en tipo diccionario como json

                elif isinstance(response_object, APIException):
                    # Get the Status
                    print("Status: " + response_object.get_status().get_value())

                    # Get the Code
                    print("Code: " + response_object.get_code().get_value())

                    print("Details")

                    # Get the details dict
                    details = response_object.get_details()

                    for key, value in details.items():
                        print(key + ' : ' + str(value))

                    # Get the Message
                    print("Message: " + response_object.get_message().get_value())
 