import psycopg2
import pandas as pd
import numpy as np

"""
Update tables
ALTER TABLE ensembles ADD COLUMN project_id integer;
ALTER TABLE ensembles ADD COLUMN created timestamp;
ALTER TABLE ensembles ADD COLUMN modified timestamp;
"""


class rti_sql:

    def __init__(self, conn):
        """
        Make a connection to the database
        :param conn: "host='localhost' dbname='my_database' user='postgres' password='secret'"
        """
        self.conn_string = conn
        self.conn = None
        self.cursor = None

        # Make a connection
        self.sql_conn(conn)

    def sql_conn(self, conn_string):
        # print the connection string we will use to connect
        print("Connecting to database\n	->%s" % (conn_string))

        # get a connection, if a connect cannot be made an exception will be raised here
        self.conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        self.cursor = self.conn.cursor()
        print("Connected!\n")

    def close(self):
        self.cursor.close()
        self.conn.close()

    def query(self, query):
        """
        Send the query and get the results from the query
        :param query: Query to execute on the database.
        :return: Results of query.  It is iterable.
        """
        print(query)
        self.cursor.execute(query)      # Send query
        self.conn.commit()

        # Return the results
        return self.cursor.fetchall()

    def insert(self, query):
        """
        Send the query to insert data.  There is no fetch with an insert.
        :param query: Query to execute on the database.
        :return: Results of query.  It is iterable.
        """
        print(query)
        self.cursor.execute(query)      # Send query to insert data
        self.conn.commit()

    def execute(self, query):
        return self.cursor.execute(query)

    def commit(self):
        return self.conn.commit()

    def create_tables(self):
        # Project
        self.cursor.execute('CREATE TABLE IF NOT EXISTS projects (id SERIAL PRIMARY KEY, '
                            'name text NOT NULL, '
                            'path text,'
                            'meta json,'
                            'created timestamp, '
                            'modified timestamp);')
        print("Projects table created")

        # Ensemble Tables
        # Ensemble
        self.cursor.execute('CREATE TABLE IF NOT EXISTS ensembles (id SERIAL PRIMARY KEY, '
                            'ensNum integer NOT NULL, '
                            'numBins integer, '
                            'numBeams integer, '
                            'desiredPings integer, '
                            'actualPings integer, '
                            'status integer, '
                            'dateTime timestamp, '
                            'serialNumber text, '
                            'firmware text,'
                            'subsystemCode character,'
                            'subsystemConfig integer, '
                            'rangeFirstBin real, '
                            'binSize real, '
                            'firstPingTime real, '
                            'lastPingTime real, '
                            'heading real, '
                            'pitch real, '
                            'roll real, '
                            'waterTemp real, '
                            'sysTemp real, '
                            'salinity real, '
                            'pressure real, '
                            'xdcrDepth real, '
                            'sos real, '
                            'rawMagFieldStrength real,'
                            'pitchGravityVector real, '
                            'rollGravityVector real, '
                            'verticalGravityVector real, '
                            'BtSamplesPerSecond real, '
                            'BtSystemFreqHz real, '
                            'BtCPCE real, '
                            'BtNCE real, '
                            'BtRepeatN real, '
                            'WpSamplesPerSecond real, '
                            'WpSystemFreqHz real, '
                            'WpCPCE real, '
                            'WpNCE real, '
                            'WpRepeatN real, '
                            'WpLagSamples real, '
                            'Voltage real, '
                            'XmtVoltage real, '
                            'BtBroadband real, '
                            'BtLagLength real, '
                            'BtNarrowband real, '
                            'BtBeamMux real, '
                            'WpBroadband real, '
                            'WpLagLength real, '
                            'WpTransmitBandwidth real, '
                            'WpReceiveBandwidth real, '
                            'burstNum integer, '
                            'project_id integer, '
                            'meta json,'
                            'created timestamp, '
                            'modified timestamp);')
        print("Ensemble Table created")

        # Bottom Track
        self.cursor.execute('CREATE TABLE IF NOT EXISTS bottomtrack (id SERIAL PRIMARY KEY,'
                            'ensIndex integer NOT NULL, '
                            'firstPingTime real, '
                            'lastPingTime real, '
                            'heading real, '
                            'pitch real, '
                            'roll real, '
                            'waterTemp real, '
                            'salinity real, '
                            'xdcrDepth real, '
                            'pressure real, '
                            'sos real, '
                            'status integer, '
                            'numBeams integer, '
                            'pingCount integer, '
                            'rangeBeam0 real, '
                            'rangeBeam1 real, '
                            'rangeBeam2 real, '
                            'rangeBeam3 real, '
                            'snrBeam0 real, '
                            'snrBeam1 real, '
                            'snrBeam2 real, '
                            'snrBeam3 real, '
                            'ampBeam0 real, '
                            'ampBeam1 real, '
                            'ampBeam2 real, '
                            'ampBeam3 real, '
                            'corrBeam0 real, '
                            'corrBeam1 real, '
                            'corrBeam2 real, '
                            'corrBeam3 real, '
                            'beamVelBeam0 real, '
                            'beamVelBeam1 real, '
                            'beamVelBeam2 real, '
                            'beamVelBeam3 real, '
                            'beamGoodBeam0 integer, '
                            'beamGoodBeam1 integer, '
                            'beamGoodBeam2 integer, '
                            'beamGoodBeam3 integer, '
                            'instrVelBeam0 real, '
                            'instrVelBeam1 real, '
                            'instrVelBeam2 real, '
                            'instrVelBeam3 real, '
                            'instrGoodBeam0 integer, '
                            'instrGoodBeam1 integer, '
                            'instrGoodBeam2 integer, '
                            'instrGoodBeam3 integer, '
                            'earthVelBeam0 real, '
                            'earthVelBeam1 real, '
                            'earthVelBeam2 real, '
                            'earthVelBeam3 real, '
                            'earthGoodBeam0 integer, '
                            'earthGoodBeam1 integer, '
                            'earthGoodBeam2 integer, '
                            'earthGoodBeam3 integer, '
                            'snrPulseCoherentBeam0 real, '
                            'snrPulseCoherentBeam1 real, '
                            'snrPulseCoherentBeam2 real, '
                            'snrPulseCoherentBeam3 real, '
                            'ampPulseCoherentBeam0 real, '
                            'ampPulseCoherentBeam1 real, '
                            'ampPulseCoherentBeam2 real, '
                            'ampPulseCoherentBeam3 real, '
                            'velPulseCoherentBeam0 real, '
                            'velPulseCoherentBeam1 real, '
                            'velPulseCoherentBeam2 real, '
                            'velPulseCoherentBeam3 real, '
                            'noisePulseCoherentBeam0 real, '
                            'noisePulseCoherentBeam1 real, '
                            'noisePulseCoherentBeam2 real, '
                            'noisePulseCoherentBeam3 real, '
                            'corrPulseCoherentBeam0 real, '
                            'corrPulseCoherentBeam1 real, '
                            'corrPulseCoherentBeam2 real, '
                            'corrPulseCoherentBeam3 real, '
                            'meta json,'
                            'created timestamp, '
                            'modified timestamp);')
        print("Bottom Track table created")

        # Bottom Track
        self.cursor.execute('CREATE TABLE IF NOT EXISTS rangetracking (id SERIAL PRIMARY KEY,'
                            'ensIndex integer NOT NULL, '
                            'numBeams integer, '
                            'snrBeam0 real, '
                            'snrBeam1 real, '
                            'snrBeam2 real, '
                            'snrBeam3 real, '
                            'rangeBeam0 real, '
                            'rangeBeam1 real, '
                            'rangeBeam2 real, '
                            'rangeBeam3 real, '
                            'pingsBeam0 integer, '
                            'pingsBeam1 integer, '
                            'pingsBeam2 integer, '
                            'pingsBeam3 integer, '
                            'amplitudeBeam0 real, '
                            'amplitudeBeam1 real, '
                            'amplitudeBeam2 real, '
                            'amplitudeBeam3 real, '
                            'correlationBeam0 real, '
                            'correlationBeam1 real, '
                            'correlationBeam2 real, '
                            'correlationBeam3 real, '
                            'beamVelocityBeam0 real, '
                            'beamVelocityBeam1 real, '
                            'beamVelocityBeam2 real, '
                            'beamVelocityBeam3 real, '
                            'instrVelBeam0 real, '
                            'instrVelBeam1 real, '
                            'instrVelBeam2 real, '
                            'instrVelBeam3 real, '
                            'earthVelBeam0 real, '
                            'earthVelBeam1 real, '
                            'earthVelBeam2 real, '
                            'earthVelBeam3 real, '
                            'meta json,'
                            'created timestamp, '
                            'modified timestamp);')
        print("Range Tracking table created")

        # Beam Velocity
        query = 'CREATE TABLE IF NOT EXISTS beamVelocity (id SERIAL PRIMARY KEY, ' \
                'ensIndex integer NOT NULL, ' \
                'beam integer NOT NULL, ' \
                'meta json,' \
                'created timestamp, ' \
                'modified timestamp, '
        for ensBin in range(0, 200):
            query += 'Bin' + str(ensBin) + ' real, '

        query = query[:-2]          # Remove final comma
        query += ');'
        self.cursor.execute(query)
        print("Beam Velocity table created")

        # Instrument Velocity
        query = 'CREATE TABLE IF NOT EXISTS instrumentVelocity (id SERIAL PRIMARY KEY, ' \
                'ensIndex integer NOT NULL, ' \
                'beam integer NOT NULL, ' \
                'meta json,' \
                'created timestamp, ' \
                'modified timestamp, '
        for ensBin in range(0, 200):
            query += 'Bin' + str(ensBin) + ' real, '

        query = query[:-2]          # Remove final comma
        query += ');'
        self.cursor.execute(query)
        print("Instrument Velocity table created")

        # Earth Velocity
        query = 'CREATE TABLE IF NOT EXISTS earthVelocity (id SERIAL PRIMARY KEY, ' \
                'ensIndex integer NOT NULL, ' \
                'beam integer NOT NULL, ' \
                'meta json,' \
                'created timestamp, ' \
                'modified timestamp, '
        for ensBin in range(0, 200):
            query += 'Bin' + str(ensBin) + ' real, '

        query = query[:-2]          # Remove final comma
        query += ');'
        self.cursor.execute(query)
        print("Earth Velocity table created")

        # Amplitude
        query = 'CREATE TABLE IF NOT EXISTS amplitude (id SERIAL PRIMARY KEY, ' \
                'ensIndex integer NOT NULL, ' \
                'beam integer NOT NULL, ' \
                'meta json,' \
                'created timestamp, ' \
                'modified timestamp, '
        for ensBin in range(0, 200):
            query += 'Bin' + str(ensBin) + ' real, '

        query = query[:-2]          # Remove final comma
        query += ');'
        self.cursor.execute(query)
        print("Amplitude table created")

        # Correlation
        query = 'CREATE TABLE IF NOT EXISTS correlation (id SERIAL PRIMARY KEY, ' \
                'ensIndex integer NOT NULL, ' \
                'beam integer NOT NULL, ' \
                'meta json,' \
                'created timestamp, ' \
                'modified timestamp, '
        for ensBin in range(0, 200):
            query += 'Bin' + str(ensBin) + ' real, '

        query = query[:-2]          # Remove final comma
        query += ');'
        self.cursor.execute(query)
        print("Correlation table created")

        # Good Beam Ping
        query = 'CREATE TABLE IF NOT EXISTS goodBeamPing (id SERIAL PRIMARY KEY, ' \
                'ensIndex integer NOT NULL, ' \
                'beam integer NOT NULL, ' \
                'meta json,' \
                'created timestamp, ' \
                'modified timestamp, '
        for ensBin in range(0, 200):
            query += 'Bin' + str(ensBin) + ' integer, '

        query = query[:-2]          # Remove final comma
        query += ');'
        self.cursor.execute(query)
        print("Good Beam Ping table created")

        # Good Earth Ping
        query = 'CREATE TABLE IF NOT EXISTS goodEarthPing (id SERIAL PRIMARY KEY, ' \
                'ensIndex integer NOT NULL, ' \
                'beam integer NOT NULL, ' \
                'meta json,' \
                'created timestamp, ' \
                'modified timestamp, '
        for ensBin in range(0, 200):
            query += 'Bin' + str(ensBin) + ' integer, '

        query = query[:-2]          # Remove final comma
        query += ');'
        self.cursor.execute(query)
        print("Good Earth Ping table created")

        # NMEA
        query = 'CREATE TABLE IF NOT EXISTS nmea (id SERIAL PRIMARY KEY, ' \
                'ensIndex integer NOT NULL, ' \
                'nmea text, ' \
                'GPGGA text, ' \
                'GPVTG text,' \
                'GPRMC text, ' \
                'GPRMF text, ' \
                'GPGLL text, ' \
                'GPGSV text, ' \
                'GPGSA text, ' \
                'GPHDT text,' \
                'GPHDG text,' \
                'latitude DECIMAL(8,6), ' \
                'longitude DECIMAL(9,6), ' \
                'speed_knots real, ' \
                'heading real, ' \
                'meta json,' \
                'datetime timestamp, ' \
                'created timestamp, ' \
                'modified timestamp);'
        self.cursor.execute(query)
        print("NMEA table created")

        print("Table Creation Complete")
        self.conn.commit()

    def ss_query(self, ss_code=None, ss_config=None):
        """
        Create a query string for the subsystem code and subsystem configuration.
        If no values are given, then empty strings are created.
        :param ss_code: Subsystem Code.
        :param ss_config: Subsystem Configuration.
        :return: Subsystem Code Query Str, Subsystem Config Index Query Str
        """

        # Use Subsystem code if given
        if ss_code:
            ss_code_str = "AND ensembles.subsystemcode = \'{}\'".format(ss_code)
        else:
            ss_code_str = ""

        # Use Subsystem configuration if given
        if ss_config:
            ss_config_str = "AND ensembles.subsystemconfig = {} ".format(ss_config)
        else:
            ss_config_str = ""

        return ss_code_str, ss_config_str

    def get_earth_vel_data(self, project_idx, beam, ss_code=None, ss_config=None):
        """
        Get all the earth velocity data for the given project and beam.
        :param project_idx: Project index.
        :param beam: Beam number.
        :param ss_code: Subsystem Code.
        :param ss_config: Subsystem Configuration.
        :return: Earth velocity data for beam in the project.
        """

        # Create the string of bins for query
        bin_nums = ""
        for x in range(0, 200):
            bin_nums += "bin" + str(x) + ", "
        bin_nums = bin_nums[:-2]  # Remove final comma

        """
        # Use Subsystem code if given
        if ss_code:
            ss_code_str = "AND ensembles.subsystemcode = \'{}\'".format(ss_code)
        else:
            ss_code_str = ""

        # Use Subsystem configuration if given
        if ss_config:
            ss_config_str = "AND ensembles.subsystemconfig = {} ".format(ss_config)
        else:
            ss_config_str = ""
        """
        ss_code_str, ss_config_str = self.ss_query(ss_code, ss_config)

        # Get all projects
        try:
            # Get all the ensembles for the project
            ens_query = 'SELECT ensembles.ensnum, ensembles.numbeams, ensembles.numbins, earthvelocity.beam, {} ' \
                        'FROM ensembles ' \
                        'INNER JOIN earthvelocity ON ensembles.id = earthvelocity.ensindex ' \
                        'WHERE ensembles.project_id = %s AND earthvelocity.beam = %s ' \
                        '{} {}' \
                        'ORDER BY ensembles.ensnum ASC;'.format(bin_nums, ss_code_str, ss_config_str)
            print(ens_query)
            self.cursor.execute(ens_query, (project_idx, beam))
            vel_results = self.cursor.fetchall()
            self.conn.commit()

        except Exception as e:
            print("Unable to run query", e)
            return

        # Make a dataframe
        df = pd.DataFrame(vel_results)
        if not df.empty:
            columns = ['ensnum', 'numbeams', 'numbins', 'beam']
            for x in range(0, 200):
                columns.append('bin' + str(x))
            df.columns = columns
            #print(df.head())

        return df

    def get_bottom_track_vel(self, project_idx):
        """
        Get Bottom track velocities.
        :param project_idx: Project index.
        :return: Dataframe with all the velocities. (Beam, Instrument and Earth)
        """

        # Get all projects
        try:
            # Get all the ensembles for the project
            ens_query = 'SELECT ensembles.ensnum, ensembles.numbins, ' \
                        'beamvelbeam0, beamvelbeam1, beamvelbeam2, beamvelbeam3, ' \
                        'instrvelbeam0, instrvelbeam1, instrvelbeam2, instrvelbeam3, ' \
                        'earthvelbeam0, earthvelbeam1, earthvelbeam2, earthvelbeam3 ' \
                        'FROM ensembles ' \
                        'INNER JOIN bottomtrack ON ensembles.id = bottomtrack.ensindex ' \
                        'WHERE ensembles.project_id = %s ORDER BY ensembles.ensnum ASC;'
            self.cursor.execute(ens_query, (project_idx,))
            vel_results = self.cursor.fetchall()
            self.conn.commit()

        except Exception as e:
            print("Unable to run query", e)
            return

        if vel_results:
            # Make a dataframe
            df = pd.DataFrame(vel_results)
            df.columns = ['ensnum', 'numbins', 'Beam0', 'Beam1', 'Beam2', 'Beam3', 'Instr0', 'Instr1', 'Instr2', 'Instr3', 'Earth0', 'Earth1', 'Earth2', 'Earth3']
        else:
            df = pd.DataFrame()

        return df

    def get_bottom_track_range(self, project_idx, ss_code=None, ss_config=None):
        """
        Get Bottom track Range.
        :param project_idx: Project index.
        :param ss_code: Subsystem Code.
        :param ss_config: Subsystem Configuration.
        :return: Dataframe with all the velocities. (Beam, Instrument and Earth)
        """

        # Set the Subsystem query
        ss_code_str, ss_config_str = self.ss_query(ss_code, ss_config)

        # Get all projects
        try:
            # Get all the ensembles for the project
            ens_query = 'SELECT ensembles.ensnum, ensembles.numbeams, ensembles.numbins, ' \
                        'ensembles.binsize, ensembles.rangefirstbin, ' \
                        'rangebeam0, rangebeam1, rangebeam2, rangebeam3 ' \
                        'FROM ensembles ' \
                        'INNER JOIN bottomtrack ON ensembles.id = bottomtrack.ensindex ' \
                        'WHERE ensembles.project_id = %s ' \
                        '{} {}' \
                        'ORDER BY ensembles.ensnum ASC;'.format(ss_code_str, ss_config_str)
            self.cursor.execute(ens_query, (project_idx,))
            vel_results = self.cursor.fetchall()
            self.conn.commit()

        except Exception as e:
            print("Unable to run query", e)
            return

        # Make a dataframe
        df = pd.DataFrame(vel_results)
        if not df.empty:
            df.columns = ['ensnum', 'NumBeams', 'NumBins', 'BinSize', 'RangeFirstBin', 'RangeBeam0', 'RangeBeam1', 'RangeBeam2', 'RangeBeam3']

        return df

    def get_adcp_info(self, project_idx):
        """
        Get information about the ensemble data.
        :param project_idx: Project index.
        :return: Earth velocity data for beam in the project.
        """

        # Get all projects
        try:
            # Get all the ensembles for the project
            ens_query = 'SELECT ensnum, datetime, serialnumber, firmware, numbins, numbeams, subsystemconfig FROM ensembles WHERE project_id = %s ORDER BY ensnum ASC;'
            self.cursor.execute(ens_query, (project_idx,))
            results = self.cursor.fetchall()
            self.conn.commit()

            ens_data = {}
            ens_data['ensnum'] = results[0][0]
            ens_data['datetime'] = results[0][1]
            ens_data['serialnumber'] = results[0][2]
            ens_data['firmware'] = results[0][3]
            ens_data['numbins'] = results[0][4]
            ens_data['numbeams'] = results[0][5]
            ens_data['subsystemconfig'] = results[0][6]

        except Exception as e:
            print("Unable to run query", e)
            return

        return ens_data

    def get_compass_data(self, project_idx, ss_code=None, ss_config=None):
        """
        Get compass ensemble data.
        :param project_idx: Project index.
        :return: Compass data in the project.
        """

        # Set the Subsystem query
        ss_code_str, ss_config_str = self.ss_query(ss_code, ss_config)

        # Get all projects
        try:
            # Get all the ensembles for the project
            ens_query = 'SELECT ensnum, datetime, heading, pitch, roll  FROM ensembles ' \
                        'WHERE ensembles.project_id = %s ' \
                        '{} {}' \
                        'ORDER BY ensembles.ensnum ASC;'.format(ss_code_str, ss_config_str)
            self.cursor.execute(ens_query, (project_idx,))
            results = self.cursor.fetchall()
            self.conn.commit()

            df = pd.DataFrame(results)
            df.columns = ['ensnum', 'datetime', 'heading', 'pitch', 'roll']

        except Exception as e:
            print("Unable to run query", e)
            return

        return df

    def get_voltage_data(self, project_idx, ss_code=None, ss_config=None):
        """
        Get voltage ensemble data.
        :param project_idx: Project index.
        :return: Compass data in the project.
        """

        # Set the Subsystem query
        ss_code_str, ss_config_str = self.ss_query(ss_code, ss_config)

        # Get all projects
        try:
            # Get all the ensembles for the project
            ens_query = 'SELECT ensnum, datetime, voltage  FROM ensembles ' \
                        'WHERE ensembles.project_id = %s ' \
                        '{} {}' \
                        'ORDER BY ensembles.ensnum ASC;'.format(ss_code_str, ss_config_str)
            self.cursor.execute(ens_query, (project_idx,))
            results = self.cursor.fetchall()
            self.conn.commit()

            df = pd.DataFrame(results)
            df.columns = ['ensnum', 'datetime', 'voltage']

        except Exception as e:
            print("Unable to run query", e)
            return

        return df


    def get_subsystem_configs(self, project_idx):
        """
        Get compass ensemble data.
        :param project_idx: Project index.
        :return: Compass data in the project.
        """

        # Get all projects
        try:
            # Get all the ensembles for the project
            ens_query = 'SELECT subsystemcode, subsystemconfig  FROM ensembles WHERE project_id = %s ORDER BY ensnum ASC;'
            self.cursor.execute(ens_query, (project_idx,))
            results = self.cursor.fetchall()
            self.conn.commit()

            df = pd.DataFrame(results)
            df.columns = ['subsystemcode', 'subsystemconfig']

        except Exception as e:
            print("Unable to run query", e)
            return

        #codes = df.subsystemcode.unique()
        #configs = df.subsystemconfig.unique()
        #configs = pd.unique(df['subsystemcode', 'subsystemconfig'].values.ravel())

        return df.drop_duplicates()

if __name__ == "__main__":
    #conn_string = "host='localhost' port='5432' dbname='rti' user='test' password='123456'"
    conn_string = "host='184.177.73.234' port='32770' dbname='rti' user='rowetech' password='rowetechinc123'"
    sql = rti_sql(conn_string)
    sql.create_tables()
    sql.close()



"""
Delete all tables.

DROP TABLE projects;
DROP TABLE amplitude;
DROP TABLE beamvelocity;
DROP TABLE bottomtrack;
DROP TABLE rangetracking;
DROP TABLE correlation;
DROP TABLE earthvelocity;
DROP TABLE ensembles;
DROP TABLE goodbeamping;
DROP TABLE goodearthping;
DROP TABLE instrumentvelocity;
DROP TABLE nmea;
"""

"""
Remove all data from all tables.

DELETE FROM projects;
DELETE FROM amplitude;
DELETE FROM beamvelocity;
DELETE FROM bottomtrack;
DELETE FROM rangetracking;
DELETE FROM correlation;
DELETE FROM earthvelocity;
DELETE FROM ensembles;
DELETE FROM goodbeamping;
DELETE FROM goodearthping;
DELETE FROM instrumentvelocity;
DELETE FROM nmea;


"""
