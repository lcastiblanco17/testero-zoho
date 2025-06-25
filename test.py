#Librerias necesarias para crear el bulk read de trabajo
import os
from zcrmsdk.src.com.zoho.crm.api.bulk_read import *
from zcrmsdk.src.com.zoho.crm.api.util import Choice
class BulkRead(object):
    @staticmethod
    def create_bulk_read_job(module_api_name):

        """
        This method is used to create a bulk read job to export records.
        :param module_api_name: The API Name of the record's module
        """

        """
        example
        module_api_name = 'Leads'
        """

        # Get instance of BulkReadOperations Class
        bulk_read_operations = BulkReadOperations()

        # Get instance of RequestWrapper Class that will contain the request body
        #en este parametro le vamos a especificar la consulta que vamos a hacer teniendo en cuenta las varibales que vamos definiendo como el modulo, paginas, columnas a estraer, en caso de que querramos hacer un filtrado tambien
        request = RequestWrapper()

        # Get instance of CallBack Class
        #Aqui definimos donde queremos que el servidor nos envie las respuestas que no va a dar el servidor, de donde extraeremos parametros como el job-id entre otros
        call_back = CallBack()

        # Set valid callback URL
        #Donde queremos que llegue la respuesta
        call_back.set_url("https://www.example.com/callback")

        # Set the HTTP method of the callback URL. The allowed value is post.
        #En este caso como vamos a crear el trabajo vamos a hacer todos los requerimientos http  de tipo post
        call_back.set_method(Choice('post'))

        # The Bulk Read Job's details is posted to this URL on successful completion / failure of the job.
        # Aqui consultamos el estado del trabajo, en que fase se encuentra o si ya se completo exitosamente
        request.set_callback(call_back)

        # Get instance of Query Class
        #buscar campo o formato de ingreso de query si es formato json como en postman o tiene un formato en especifico
        query = Query()

        # Specifies the API Name of the module to be read.
        query.set_module(module_api_name)

        # Specifies the unique ID of the custom view, whose records you want to export.
        query.set_cvid('3409643000000087501')

        # List of field names
        field_api_names = ['Last_Name']

        # Specifies the API Name of the fields to be fetched
        query.set_fields(field_api_names)

        # To set page value, By default value is 1.
        query.set_page(1)

        # Get instance of Criteria Class
        #Se le pasan los criterios en caso de que se quiera hacer una filtracion de datos en el momento de la extraccion 
        criteria = Criteria()

        # To set API name of a field
        criteria.set_api_name('Created_Time')

        # To set comparator(eg: equal, greater_than)
        criteria.set_comparator(Choice('between'))

        time = ["2020-06-03T17:31:48+05:30", "2020-06-03T17:31:48+05:30"]

        # To set the value to be compared
        criteria.set_value(time)

        # To filter the records to be exported
        query.set_criteria(criteria)

        # Set the query object
        #Basicamente lo que hace es crear el wrapper que se llama request, luego de esto formamos la query donde basicamente le pasamos todos lo parametros de la consulta e incluso podemos filtrar con el parametro criteria
        #Luego de que ya se establecio el criteria se guarda o se setea en la query y luego se setea el wrapper con la query, lo bueno es que lo hace paso a paso y es modular y no hace todo en una sola instancia
        request.set_query(query)

        # Specify the value for this key as "ics" to export all records in the Events module as an ICS file.
        # request.set_file_type(Choice('ics'))

        # Call create_bulk_read_job method that takes RequestWrapper instance as parameter
        response = bulk_read_operations.create_bulk_read_job(request)


        #Comprobamos que el request n este vacio
        if response is not None:
            # Get the status code from response
            print('Status Code: ' + str(response.get_status_code()))

            # Get object from response
            response_object = response.get_object()
            #si la respuesta que nos da el trabajo no es ta vacia
            if response_object is not None:

                # Check if expected ActionWrapper instance is received.
                #vrifica que la clase wrapper si se halla activado, en pocas palabras verifica la consulta si se realice
                if isinstance(response_object, ActionWrapper):
                    action_response_list = response_object.get_data()

                    for action_response in action_response_list:

                        # Check if the request is successful
                        #lo mism que en la celda de arriba verifica si action_reponse tiene la instncia succes
                        if isinstance(action_response, SuccessResponse):
                            # Get the Status
                            print("Status: " + action_response.get_status().get_value())

                            # Get the Code
                            print("Code: " + action_response.get_code().get_value())

                            print("Details")

                            # Get the details dict
                            details = action_response.get_details()

                            for key, value in details.items():
                                print(key + ' : ' + str(value))

                            # Get the Message
                            print("Message: " + action_response.get_message().get_value())

                        # Check if the request returned an exception
                        elif isinstance(action_response, APIException):
                            # Get the Status
                            print("Status: " + action_response.get_status().get_value())

                            # Get the Code
                            print("Code: " + action_response.get_code().get_value())

                            print("Details")

                            # Get the details dict
                            details = action_response.get_details()

                            for key, value in details.items():
                                print(key + ' : ' + str(value))

                            # Get the Message
                            print("Message: " + action_response.get_message().get_value())

                # Check if the request returned an exception
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
 