import base64
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def main(payload) -> str:
    '''Define a main() function to process data according to use-case and return a string output'''
    # TODO
    pass

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        logger.info(f"Processing Record - {record['recordId']}")
        _payload = base64.b64decode(record['data']).decode('utf-8')
        _timestamp = datetime.fromtimestamp(int(record['approximateArrivalTimestamp'])/1000.0)
        partition_keys = {
                            "year": _timestamp.strftime('%Y'),
                            "month": _timestamp.strftime('%m'),
                            "day": _timestamp.strftime('%d'),
                            "hour": _timestamp.strftime('%H')
                        }
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'metadata': {'partitionKeys': partition_keys}
        }
        try:
            resp = main(_payload)
            output_record.update({'data': base64.b64encode(resp.encode('utf-8')).decode('utf-8')})
        except Exception:
            output_record.update({
                'result': 'ProcessingFailed',
                'data': base64.b64encode(_payload.encode('utf-8')).decode('utf-8')
            })
        output.append(output_record)

    return {'records': output}