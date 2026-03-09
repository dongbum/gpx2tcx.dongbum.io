from xml.dom.minidom import Document


class TCXMaker(object):

    def __init__(self):
        self.tcx_xmldoc = Document()
        self.tcx_root_node = None
        self.course_node = None
        self.track_node = None

        tcx_node = self.tcx_xmldoc.createElement('TrainingCenterDatabase')
        tcx_node.setAttribute('xmlns', 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2')
        tcx_node.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        tcx_node.setAttribute(
            'xsi:schemaLocation',
            'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 '
            'http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd'
        )
        self.tcx_xmldoc.appendChild(tcx_node)
        self.tcx_root_node = tcx_node

        courses_node = self.tcx_xmldoc.createElement('Courses')
        tcx_node.appendChild(courses_node)

        course_node = self.tcx_xmldoc.createElement('Course')
        courses_node.appendChild(course_node)
        self.course_node = course_node

        track_node = self.tcx_xmldoc.createElement('Track')
        course_node.appendChild(track_node)
        self.track_node = track_node

    def add_name(self, name):
        course_name_node = self.tcx_xmldoc.createElement('Name')
        self.course_node.appendChild(course_name_node)

        course_name_node_text_node = self.tcx_xmldoc.createTextNode(name)
        course_name_node.appendChild(course_name_node_text_node)

        folder_node = self.tcx_xmldoc.createElement('Folders')
        self.tcx_root_node.appendChild(folder_node)

        courses_node = self.tcx_xmldoc.createElement('Courses')
        folder_node.appendChild(courses_node)

        course_folder_node = self.tcx_xmldoc.createElement('CourseFolder')
        course_folder_node.setAttribute('Name', name)
        courses_node.appendChild(course_folder_node)

        course_name_ref_node = self.tcx_xmldoc.createElement('CourseNameRef')
        course_folder_node.appendChild(course_name_ref_node)

        id_node = self.tcx_xmldoc.createElement('Id')
        course_name_ref_node.appendChild(id_node)

        id_text_node = self.tcx_xmldoc.createTextNode(name)
        id_node.appendChild(id_text_node)

    def add_lap(self, totaltime_sec, distance, begin_lat, begin_lon, end_lat, end_lon):
        lap_node = self.tcx_xmldoc.createElement('Lap')
        self.course_node.appendChild(lap_node)

        total_time_node = self.tcx_xmldoc.createElement('TotalTimeSeconds')
        lap_node.appendChild(total_time_node)
        total_time_node_text_node = self.tcx_xmldoc.createTextNode(totaltime_sec)
        total_time_node.appendChild(total_time_node_text_node)

        distance_node = self.tcx_xmldoc.createElement('DistanceMeters')
        lap_node.appendChild(distance_node)
        distance_node_text_node = self.tcx_xmldoc.createTextNode(distance)
        distance_node.appendChild(distance_node_text_node)

        begin_node = self.tcx_xmldoc.createElement('BeginPosition')
        lap_node.appendChild(begin_node)

        begin_lat_node = self.tcx_xmldoc.createElement('LatitudeDegrees')
        begin_node.appendChild(begin_lat_node)
        begin_lat_node_text_node = self.tcx_xmldoc.createTextNode(begin_lat)
        begin_lat_node.appendChild(begin_lat_node_text_node)

        begin_lon_node = self.tcx_xmldoc.createElement('LongitudeDegrees')
        begin_node.appendChild(begin_lon_node)
        begin_lon_node_text_node = self.tcx_xmldoc.createTextNode(begin_lon)
        begin_lon_node.appendChild(begin_lon_node_text_node)

        end_node = self.tcx_xmldoc.createElement('EndPosition')
        lap_node.appendChild(end_node)

        end_lat_node = self.tcx_xmldoc.createElement('LatitudeDegrees')
        end_node.appendChild(end_lat_node)
        end_node_text_node = self.tcx_xmldoc.createTextNode(end_lat)
        end_lat_node.appendChild(end_node_text_node)

        end_lon_node = self.tcx_xmldoc.createElement('LongitudeDegrees')
        end_node.appendChild(end_lon_node)
        end_lon_node_text_node = self.tcx_xmldoc.createTextNode(end_lon)
        end_lon_node.appendChild(end_lon_node_text_node)

        intensity_node = self.tcx_xmldoc.createElement('Intensity')
        lap_node.appendChild(intensity_node)
        intensity_node_text_node = self.tcx_xmldoc.createTextNode('Active')
        intensity_node.appendChild(intensity_node_text_node)

    def add_trackpoint(self, lat, lon, ele):
        trackpoint_node = self.tcx_xmldoc.createElement('TrackPoint')
        self.track_node.appendChild(trackpoint_node)

        time_node = self.tcx_xmldoc.createElement('Time')
        trackpoint_node.appendChild(time_node)
        time_text_node = self.tcx_xmldoc.createTextNode('2010-01-01T00:00:00Z')
        time_node.appendChild(time_text_node)

        position_node = self.tcx_xmldoc.createElement('Position')
        trackpoint_node.appendChild(position_node)

        lat_node = self.tcx_xmldoc.createElement('LatitudeDegrees')
        position_node.appendChild(lat_node)

        lat_text_node = self.tcx_xmldoc.createTextNode(lat)
        lat_node.appendChild(lat_text_node)

        lon_node = self.tcx_xmldoc.createElement('LongitudeDegrees')
        position_node.appendChild(lon_node)

        lon_text_node = self.tcx_xmldoc.createTextNode(lon)
        lon_node.appendChild(lon_text_node)

        alt_node = self.tcx_xmldoc.createElement('AltitudeMeters')
        trackpoint_node.appendChild(alt_node)

        alt_text_node = self.tcx_xmldoc.createTextNode(ele)
        alt_node.appendChild(alt_text_node)

        dist_node = self.tcx_xmldoc.createElement('DistanceMeters')
        trackpoint_node.appendChild(dist_node)

    def add_coursepoint(self, lat, lon, wpt_name):
        coursepoint_node = self.tcx_xmldoc.createElement('CoursePoint')
        self.course_node.appendChild(coursepoint_node)

        wpt_name_node = self.tcx_xmldoc.createElement('Name')
        coursepoint_node.appendChild(wpt_name_node)

        wpt_name_text_node = self.tcx_xmldoc.createTextNode(wpt_name)
        wpt_name_node.appendChild(wpt_name_text_node)

        time_node = self.tcx_xmldoc.createElement('Time')
        coursepoint_node.appendChild(time_node)

        time_text_node = self.tcx_xmldoc.createTextNode('2010-01-01T01:26:32Z')
        time_node.appendChild(time_text_node)

        position_node = self.tcx_xmldoc.createElement('Position')
        coursepoint_node.appendChild(position_node)

        lat_node = self.tcx_xmldoc.createElement('LatitudeDegrees')
        position_node.appendChild(lat_node)

        lat_text_node = self.tcx_xmldoc.createTextNode(lat)
        lat_node.appendChild(lat_text_node)

        lon_node = self.tcx_xmldoc.createElement('LongitudeDegrees')
        position_node.appendChild(lon_node)

        lon_text_node = self.tcx_xmldoc.createTextNode(lon)
        lon_node.appendChild(lon_text_node)

        pointtype_node = self.tcx_xmldoc.createElement('PointType')
        coursepoint_node.appendChild(pointtype_node)

        pointtype_text_node = self.tcx_xmldoc.createTextNode('Generic')
        pointtype_node.appendChild(pointtype_text_node)

    def get_tcx(self):
        return self.tcx_xmldoc.toprettyxml(encoding='UTF-8')
