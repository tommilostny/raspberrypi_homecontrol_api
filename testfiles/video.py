#### Videos endpoint ####
from flask_restful import Resource, reqparse, abort

videos = {}
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

def abort_video_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message="Video with this ID does not exist...")

def abort_video_exists(video_id):
    if video_id in videos:
        abort(409, message="Video with this ID already exists...")

class Video(Resource):
    def get(self, video_id):
        abort_video_doesnt_exist(video_id)
        return videos[video_id]

    def put(self, video_id):
        abort_video_exists(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201

    def delete(self, video_id):
        abort_video_doesnt_exist(video_id)
        del videos[video_id]
        return '',204
#### End of videos endpoint ####