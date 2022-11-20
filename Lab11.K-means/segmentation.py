import numpy as np
import cv2
import tqdm
import os

# color of different clusters
GBR = [[0, 0, 255],
       [0, 128, 255],
       [255, 0, 0],
       [128, 0, 128],
       [255, 0, 255]]

# path configuration
project_root = os.path.split(__file__)[0]
output_path = os.path.join(project_root, "data", "result")
input_path = os.path.join(project_root, "data", "original")


def update_seed(n_cl, label, distance):
    """
        update seeds

    :param n_cl:        number of classes
    :param label:       labels
    :param distance:    distance between samples and centroids
    :return:            new seeds
    """
    seeds = np.zeros((n_cl,))
    # TODO: update seeds

    return seeds.astype(int)


def kmeans(data: np.ndarray, n_cl: int, seeds: np.ndarray = None):
    """
        K-means

    :param data:    original data
    :param n_cl:    number of classes
    :param seeds:   seeds
    :return:        new labels and new seeds
    """
    n_samples, channel = data.shape

    # TODO: firstly you should init centroids by a certain strategy
    centers = None

    old_labels = np.zeros((n_samples,))
    new_seeds = None
    while True:
        # TODO: calc distance between samples and centroids
        distance = None

        # TODO: classify samples
        new_labels = old_labels

        # TODO: update centroids
        centers = centers

        if np.all(new_labels == old_labels):
            # use seeds to avoid frequent changes of color between different classes in adjacent frames
            # of course this code isn't compulsory, if you are interested in it, you can try

            # new_seeds = update_seed(n_cl, new_labels, distance)
            break
        old_labels = new_labels

    return old_labels, new_seeds


def detect(video, n_cl=2):
    # load video, get number of frames and get shape of frame
    cap = cv2.VideoCapture(video)
    fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # instantiate a video writer
    video_writer = cv2.VideoWriter(os.path.join(output_path, "result_with_%dclz.mp4" % n_cl),
                                   cv2.VideoWriter_fourcc(*'mp4v'),
                                   (fps / 10),
                                   size,
                                   isColor=True)

    # initialize frame and seeds
    ret, frame = cap.read()
    seeds = None

    print("Begin clustering with %d classes:" % n_cl)
    bar = tqdm.tqdm(total=fps)  # progress bar
    while ret:
        frame = np.float32(frame)
        h, w, c = frame.shape

        # k-means
        data = frame.reshape((h * w, c))
        labels, seeds = kmeans(data, n_cl=n_cl, seeds=seeds)

        # give different cluster different colors
        new_frame = np.zeros((h * w, c))
        # TODO: dye pixels with colors
        new_frame = new_frame.reshape((h, w, c)).astype("uint8")
        video_writer.write(new_frame)

        ret, frame = cap.read()
        bar.update()

    # release resources
    video_writer.release()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_sample = os.path.join(input_path, "road_video.MOV")

    detect(video_sample, n_cl=1)
