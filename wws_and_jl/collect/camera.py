import io
import time
import threading
# from PIL import Image
# import picamera  ## 无树莓派测试时需要将该行注释

try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class CameraEvent(object):
    """An Event-like class that signals all active clients when a new frame is
    available.
    """

    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class BaseCamera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    event = CameraEvent()

    def __init__(self):
        """Start the background camera thread if it isn't running yet."""
        if BaseCamera.thread is None:
            BaseCamera.last_access = time.time()

            # start background frame thread
            BaseCamera.thread = threading.Thread(target=self._thread)
            BaseCamera.thread.start()

            # wait until frames are available
            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        """Return the current camera frame."""
        BaseCamera.last_access = time.time()

        # wait for a signal from the camera thread
        BaseCamera.event.wait()
        BaseCamera.event.clear()

        return BaseCamera.frame

    @staticmethod
    def frames():
        """"Generator that returns frames from the camera."""
        raise RuntimeError("Must be implemented by subclasses.")

    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print("Starting camera thread.")
        frames_iterator= cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()  # send signal to clients
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                print("Stopping camera thread due to inactivity.")
                break
        BaseCamera.thread = None


class Camera(BaseCamera):
    def __init__(self):
        # 加载样本图片并学习如何识别它。
        obama_image = face_recognition.load_image_file("pictures/obama.jpeg")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        biden_image = face_recognition.load_image_file("pictures/biden.jpeg")
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

        saltfish_image = face_recognition.load_image_file("pictures/saltfish.png")
        saltfish_face_encoding = face_recognition.face_encodings(saltfish_image)[0]

        # 创建已知面部编码及其名称的数组
        known_face_encodings = [
            obama_face_encoding,
            biden_face_encoding,
            saltfish_face_encoding,
        ]
        known_face_names = ["Barack Obama", "Joe Biden", "Salt Fish"]

        # 初始化一些变量
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

    @classmethod
    def _process_images(cls):
        # 查找当前视频帧中的所有面部和面部编码
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations
        )

        face_names = []
        for face_encoding in face_encodings:
            # 查看面孔是否与已知面孔相匹配
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding, tolerance=0.6
            )
            name = "Unknown"
            # 使用距离新脸最近的已知脸
            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding
            )
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            # 由于处理前缩小了尺寸，这里放大
            face_locations = (np.array(face_locations) * 4).tolist()
            # 记录下每个面部的位置
            frame_images = []
            for (top, right, bottom, left) in face_locations:
                frame_images.append(frame[top:bottom, left:right])
            frame = cv2.GaussianBlur(frame, (99, 99), 30)
            for (top, right, bottom, left), frame_img in zip(
                face_locations, frame_images
            ):
                frame[top:bottom, left:right] = frame_img

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # 在脸上画一个框
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # 在面部下方绘制名称标签
                cv2.rectangle(
                    frame,
                    (left, bottom - 35),
                    (right, bottom),
                    (0, 0, 255),
                    cv2.FILLED,
                )
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(
                    frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1,
                )
            # 显示结果图像
            cv2.imshow("Video", frame)

        @staticmethod
        def frames():
            with picamera.PiCamera() as camera:
                camera.hflip = False  # 是否进行水平翻转
                camera.vflip = False  # 是否进行垂直翻转
                camera.rotation = 180  # 是否对图像进行旋转
                # let camera warm up
                time.sleep(2)

                stream = io.BytesIO()
                for _ in camera.capture_continuous(stream, "jpeg", use_video_port=True):
                    # return current frame

                    stream.seek(0)
                    image = Image.open(stream)

                    yield stream.read()

                    # reset stream for next frame
                    stream.seek(0)
                    stream.truncate()


class CameraTest(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""

    imgs = [
        open(f + ".jpg", "rb").read()
        for f in [
            "wws_and_jl/collect/images/1",
            "wws_and_jl/collect/images/2",
            "wws_and_jl/collect/images/3",
        ]
    ]

    @staticmethod
    def frames():
        while True:
            time.sleep(1)
            yield CameraTest.imgs[int(time.time()) % 3]
