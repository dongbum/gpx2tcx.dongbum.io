from io import BytesIO

from flask import render_template, request, send_file
from gpx2tcx.blueprint import gpx2tcx
from gpx2tcx.controller.tcxmaker import TCXMaker
from xml.dom import minidom

ALLOWED_EXTENSIONS = {"gpx"}


def _allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@gpx2tcx.route('/upload')
def upload():
    return render_template('upload.html')


@gpx2tcx.route('/upload_process', methods=['POST'])
def upload_process():
    upload_gpx = request.files.get('gpxfile')

    if not upload_gpx or not upload_gpx.filename:
        return render_template('upload.html', error='GPX ??? ??? ???.'), 400

    if not _allowed_file(upload_gpx.filename):
        return render_template('upload.html', error='gpx ??? ??? ???? ? ????.'), 400

    try:
        gpx_xmldoc = minidom.parse(upload_gpx.stream).documentElement

        tcx_maker = TCXMaker()

        wpt_items = gpx_xmldoc.getElementsByTagName('wpt')
        for wpt_item in wpt_items:
            wpt_name_nodes = wpt_item.getElementsByTagName('name')
            wpt_name = wpt_name_nodes[0].firstChild.data if wpt_name_nodes and wpt_name_nodes[0].firstChild else 'Waypoint'
            tcx_maker.add_coursepoint(wpt_item.getAttribute('lat'), wpt_item.getAttribute('lon'), wpt_name)

        trk_items = gpx_xmldoc.getElementsByTagName('trk')
        if not trk_items:
            return render_template('upload.html', error='?? ??(trk)? ?? GPX ?????.'), 400

        trk_name_nodes = trk_items[0].getElementsByTagName('name')
        course_name = trk_name_nodes[0].firstChild.data if trk_name_nodes and trk_name_nodes[0].firstChild else 'Converted Course'
        tcx_maker.add_name(course_name)

        trkseg_items = trk_items[0].getElementsByTagName('trkseg')
        if not trkseg_items:
            return render_template('upload.html', error='?? ????(trkseg)? ?? GPX ?????.'), 400

        trkpt_items = trkseg_items[0].getElementsByTagName('trkpt')
        if not trkpt_items:
            return render_template('upload.html', error='?? ???(trkpt)? ?? GPX ?????.'), 400

        begin_lat = ''
        begin_lon = ''
        end_lat = ''
        end_lon = ''

        for trkpt_item in trkpt_items:
            ele_nodes = trkpt_item.getElementsByTagName('ele')
            ele = ele_nodes[0].firstChild.data if ele_nodes and ele_nodes[0].firstChild else '0'

            lat = trkpt_item.getAttribute('lat')
            lon = trkpt_item.getAttribute('lon')
            tcx_maker.add_trackpoint(lat, lon, ele)

            if not begin_lat and not begin_lon:
                begin_lat = lat
                begin_lon = lon

            end_lat = lat
            end_lon = lon

        tcx_maker.add_lap('0', '0', begin_lat, begin_lon, end_lat, end_lon)

        buffer = BytesIO()
        buffer.write(tcx_maker.get_tcx())
        buffer.seek(0)

        download_name = upload_gpx.filename.rsplit('.', 1)[0] + '.tcx'
        return send_file(buffer, as_attachment=True, download_name=download_name, mimetype='application/xml')
    except Exception:
        return render_template('upload.html', error='?? ?? ? ??? ??????.'), 500
