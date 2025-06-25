
#Librerias necesarias para hacer la comprobacion de estado del trabajo
import os
from zcrmsdk.src.com.zoho.crm.api.bulk_read import *
from zcrmsdk.src.com.zoho.crm.api.util import Choice
class BulkRead(object):
    @staticmethod
    def get_bulk_read_job_details(job_id):

        """
        This method is used to get the details of a bulk read job performed previously.
        :param job_id: The unique ID of the bulk read job.
        """

        """
        example
        job_id = 3409643000002461001
        """

        # Get instance of BulkReadOperations Class
        #Define igual que en la creacion del trabajo la instancia de bulkread
        bulk_read_operations = BulkReadOperations()

        # Call get_bulk_read_job_details method that takes jobId as parameter
        #consultamos el job_id que nos genero el bulkread anterior de la creacion
        response = bulk_read_operations.get_bulk_read_job_details(job_id)

        #Comprueba que la respuesta tenga informacion para evitar procesos mal hechos y que se verifique que se realizo y se ejecuto el codigo anterior
        if response is not None:

            # Get the status code from response
            #obtiene de nuevo el estado del job_id
            print('Status Code: ' + str(response.get_status_code()))

            # se verifica si el estado nos indica que o no hay datos o contenido, o si no se ha mdificado nada desde la ultima ejecucion(esto solo cuenta si ya se ejecuto una vez y pues creo que con los mismo parametros com page y query)
            if response.get_status_code() in [204, 304]:
                print('No Content' if response.get_status_code() == 204 else 'Not Modified')
                return

            # Get object from response
            response_object = response.get_object()

            if response_object is not None:

                # Check if expected ResponseWrapper instance is received
                #hace comprobaciones similares a las que se hacen en la parte de creacion del trabajo
                if isinstance(response_object, ResponseWrapper):

                    # Get the list of JobDetail instances
                    job_details_list = response_object.get_data()

                    for job_detail in job_details_list:
                        # Get the Job ID of each jobDetail
                        print("Bulk read Job ID: " + job_detail.get_id())

                        # Get the Operation of each jobDetail
                        print("Bulk read Operation: " + job_detail.get_operation())

                        # Get the State of each jobDetail
                        print("Bulk read State: " + job_detail.get_state().get_value())

                        # Get the Result instance of each jobDetail
                        result = job_detail.get_result()
                        #Aqui es donde obtenemos mas detalles sobre la conulta tipo pagina, conteo de filas extraidas, el url de descarga que nos pasa zoho, el numero de registros por pagina y un bool que nos dice si quedan o no mas registros
                        if result is not None:
                            # Get the Page of the Result
                            print("Bulkread Result Page: " + str(result.get_page()))

                            # Get the Count of the Result
                            print("Bulkread Result Count: " + str(result.get_count()))

                            # Get the Download URL of the Result
                            print("Bulkread Result Download URL: " + result.get_download_url())

                            # Get the Per_Page of the Result
                            print("Bulkread Result Per_Page: " + str(result.get_per_page()))

                            # Get the MoreRecords of the Result
                            print("Bulkread Result MoreRecords: " + str(result.get_more_records()))

                        # Get the Query instance of each jobDetail
                        #Obtiene informacion de la consulta que se especifico mas en cuanto al filtrado
                        query = job_detail.get_query()

                        if query is not None:
                            # Get the Module Name of the Query
                            print("Bulk read Query Module: " + query.get_module())

                            # Get the Page of the Query
                            print("Bulk read Query Page: " + str(query.get_page()))

                            # Get the cvid of the Query
                            print("Bulk read Query cvid: " + str(query.get_cvid()))

                            # Get the fields List of the Query
                            fields = query.get_fields()

                            if fields is not None:
                                print("Bulk read fields")
                                for field in fields:
                                    print(field)

                            # Get the Criteria instance of the Query
                            criteria = query.get_criteria()

                            if criteria is not None:
                                BulkRead.print_criteria(criteria)

                            # Get the CreatedBy User instance of each jobDetail
                            created_by = job_detail.get_created_by()

                            # Check if created_by is not None
                            if created_by is not None:
                                # Get the Name of the created_by User
                                print("Bulkread Created By - Name: " + created_by.get_name())

                                # Get the ID of the created_by User
                                print("Bulkread Created By - ID: " + created_by.get_id())

                            # Get the CreatedTime of each jobDetail
                            print("Bulkread CreatedTime: " + str(job_detail.get_created_time()))

                            # Get the FileType of each jobDetail
                            print("Bulkread File Type: " + job_detail.get_file_type())

                # Check if the request returned an exception
                # esto es en caso de que ocurra algun error de configuracion, etc
                # me devueve los detalles en tipo json o diccionario
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

    @staticmethod
    def print_criteria(criteria):
        if criteria.get_api_name() is not None:
            # Get the API Name of the Criteria
            print('BulkRead Criteria API Name: ' + criteria.get_api_name())

        if criteria.get_comparator() is not None:
            # Get the Comparator of the Criteria
            print('BulkRead Criteria Comparator: ' + criteria.get_comparator().get_value())

        if criteria.get_value() is not None:
            # Get the Value of the Criteria
            print('BulkRead Criteria Value: ' + str(criteria.get_value()))

        # Get the List of Criteria instance of each Criteria
        criteria_group = criteria.get_group()

        if criteria_group is not None:
            for each_criteria in criteria_group:
                BulkRead.print_criteria(each_criteria)

        if criteria.get_group_operator() is not None:
            # Get the Group Operator of the Criteria
            print('BulkRead Criteria Group Operator: ' + criteria.get_group_operator().get_value())  
 