"""
Generate a custom data stream simulation

Receive a CSV file
Write the contents row by row to a TXT file.

NOTE: the default CSV file has a delimiter of '\t' rather than ','

"""

# Imports
import csv, logging, socket, time

# Set up basic logger
logging.basicConfig(level = logging.INFO,
                    format = "%(asctime)s - %(levelname)s - %(message)s"
                    )

# Declare constants
HOST = 'localhost'
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)
SLEEP_TIMER_SEC = 3
DELIM = '\t'
INPUT_FILE = 'DRN_Nats.csv'


# Define row-reader function
def read_row(row):
    """
    Function to split the contents of a row into respective categories

    """
    # Read in the contents of the row
    round_num, question_num, point_value, question_type, answer_type, location_type, hit_point, notes = row

    # Create a format string of the row's contents
    f_str = f'[{round_num}, {question_num}, {point_value}, {question_type}, {answer_type}, {location_type}, {hit_point}, {notes}]'

    # Generate a binary message of our f string
    MSG = f_str.encode()

    logging.debug(f'Returning {f_str}')

    # Return the binary message
    return MSG


# Define streaming function
def stream_file(input_file_name, addr_tuple):
    """
    Function to read and stream the contents of a CSV file
    
    """
    
    logging.info(f'Start streaming data from {input_file_name} to {addr_tuple}')

    # Open the CSV file
    with open(input_file_name, 'r') as input_csv:

        logging.info(f'Opened file for reading: {input_file_name}')

        # Create a CSV reader object
        reader_obj = csv.reader(input_csv, delimiter=DELIM)

        # Skip the header
        header = next(reader_obj)


        # Configure our socket object
        #-> IVP4 address = internet
        #-> Socket Type = UDP datagram
        ADDRESS_FAMILY = socket.AF_INET
        SOCKET_TYPE = socket.SOCK_DGRAM

        # Call the socket constructor
        sock_obj = socket.socket(ADDRESS_FAMILY, SOCKET_TYPE)


        # Send each row to the read_row function above
        #-> for each row
        for row in reader_obj:
            # If not, check if the row empty
            if row != []:
        
                # Call the read_row function
                #-> returns binary message
                MESSAGE = read_row(row)

                logging.info(f'Sent {MESSAGE} on Port {PORT}')

                # Sleep for SLEEP_TIMER_SEC seconds
                time.sleep(SLEEP_TIMER_SEC)


# ---------------------------------------------------------------------------
# If this is the script we are running, then call some functions and execute code!
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        logging.info("===============================================")
        logging.info("Starting fake streaming process.")

        # Call stream_file function
        stream_file(INPUT_FILE, ADDRESS_TUPLE)

        logging.info("Streaming complete!")
        logging.info("===============================================")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

