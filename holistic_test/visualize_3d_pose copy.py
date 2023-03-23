import sys
import numpy as np

from PyQt6 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (5, 6), (6, 7), (7, 8),
    (9, 10), (10, 11), (11, 12),
    (13, 14), (14, 15), (15, 16),
    (17, 18), (18, 19), (19, 20),
    (0, 5), (5, 9), (9, 13), (13, 17), (0, 17)
]

POSE_CONNECTIONS = [
    (0,1), (1,2), (2,3), (3,7),
    (0,4), (4,5), (5,6), (6,8),
    (9,10),
    (11,13), (13,15), (15,17), (17,19), (19,15), (15,21),
    (12,14), (14,16), (16,18), (18,20), (20,16), (16,22),
    (11,12), (12,24), (24,23), (23,11)
]

FACE_CONNECTIONS = [
    # Lips.
    (61, 146), (146, 91), (91, 181), (181, 84), (84, 17),
    (17, 314), (314, 405), (405, 321), (321, 375), (375, 291),
    (61, 185), (185, 40), (40, 39), (39, 37), (37, 0),
    (0, 267), (267, 269), (269, 270), (270, 409), (409, 291),
    (78, 95), (95, 88), (88, 178), (178, 87), (87, 14),
    (14, 317), (317, 402), (402, 318), (318, 324), (324, 308),
    (78, 191), (191, 80), (80, 81), (81, 82), (82, 13),
    (13, 312), (312, 311), (311, 310), (310, 415), (415, 308),
    # Left eye.
    (263, 249), (249, 390), (390, 373), (373, 374), (374, 380),
    (380, 381), (381, 382), (382, 362), (263, 466), (466, 388),
    (388, 387), (387, 386), (386, 385), (385, 384), (384, 398),
    (398, 362),
    # Left eyebrow.
    (276, 283), (283, 282), (282, 295), (295, 285), (300, 293),
    (293, 334), (334, 296), (296, 336),
    # Right eye.
    (33, 7), (7, 163), (163, 144), (144, 145), (145, 153),
    (153, 154), (154, 155), (155, 133), (33, 246), (246, 161),
    (161, 160), (160, 159), (159, 158), (158, 157), (157, 173),
    (173, 133),
    # Right eyebrow.
    (46, 53), (53, 52), (52, 65), (65, 55), (70, 63), (63, 105),
    (105, 66), (66, 107),
    # Face oval.
    (10, 338), (338, 297), (297, 332), (332, 284), (284, 251),
    (251, 389), (389, 356), (356, 454), (454, 323), (323, 361),
    (361, 288), (288, 397), (397, 365), (365, 379), (379, 378),
    (378, 400), (400, 377), (377, 152), (152, 148), (148, 176),
    (176, 149), (149, 150), (150, 136), (136, 172), (172, 58),
    (58, 132), (132, 93), (93, 234), (234, 127), (127, 162),
    (162, 21), (21, 54), (54, 103), (103, 67), (67, 109),
    (109, 10)
]

HAND_PATH = [
    0, 1, 2, 3, 4, 3, 2, 1, 0, 5, 6, 7, 8, 7, 6, 5, 9, 10, 11, 12, 11,
    10, 9, 13, 14, 15,1 16, 15, 14, 13, 17, 18, 19, 20, 19, 18, 17, 0
]
POSE_PATH = [
    7, 3, 2, 1, 0, 4, 5, 6, 8, 6, 5, 4, 0, 9, 10,
    11, 12, 13, 15, 21, 15, 17, 19, 15, 13, 11, 12, 14, 16, 22, 16, 18, 20, 16, 14, 12,
    24, 26, 28, 32, 30, 28, 26, 24, 23, 25, 27, 29, 31
]
FACE_PATH = [
]

class MediaPipeVisualizer(gl.GLViewWidget) :
    def __init__(self) -> None :
        super().__init__()

        gx = gl.GLGridItem()
        gx.rotate(90, 0, 1, 0)
        #gx.translate(-1.5, 0, 0)
        self.addItem(gx)
        gy = gl.GLGridItem()
        gy.rotate(90, 1, 0, 0)
        #gy.translate(0, -1.5, 0)
        self.addItem(gy)
        gz = gl.GLGridItem()
        #gz.translate(0, 0, -1.5)
        self.addItem(gz)

        self.left_hand_line_list = []
        self.right_hand_line_list = []
        self.face_line_list = []
        self.pose_line_list = []

    def landmark2Line(self, landmark_array, connection_chain) :
        return landmark_array[[connection_chain]]

    def updateLeftHand(self, landmark_array) :
        for line_item in self.left_hand_line_list :
                self.removeItem(line_item)
        
        if len(landmark_array) :    
            line = self.landmark2Line(landmark_array, HAND_PATH)
            self.left_hand_line_list = [gl.GLLinePlotItem(
                pos = line,
                color = pg.mkColor((255, 100, 0)),
                width = 2,
                antialias = True
            )]
            for item in self.left_hand_line_list :
                if item :
                    self.addItem(item)

    def updateRightHand(self, landmark_array):
        for line_item in self.lright_hand_line_list :
                self.removeItem(line_item)
        
        if len(landmark_array) :    
            line = self.landmark2Line(landmark_array, HAND_PATH)
            self.right_hand_line_list = [gl.GLLinePlotItem(
                pos = line,
                color = pg.mkColor((100, 255, 0)),
                width = 2,
                antialias = True
            )]
            for item in self.right_hand_line_list :
                if item :
                    self.addItem(item)

    def updatePose(self, landmark_array) :
        for line_item in self.pose_line_list :
            self.removeItem(line_item)
        
        if len(landmark_array) :    
            line = self.landmark2Line(landmark_array, POSE_PATH)
            self.pose_line_list = [gl.GLLinePlotItem(
                pos = line,
                color = pg.mkColor((100, 100, 255)),
                width = 3,
                antialias = True
            )]
            for item in self.pose_line_list :
                if item :
                    self.addItem(item)

    def updateFace(self, landmark_list) :
        for line_item in self.face_line_list :
            self.removeItem(line_item)
        self.face_line_list = list(map(
            lambda connection : gl.GLLinePlotItem(
                pos = np.array([
                    landmark_list[connection[0]],
                    landmark_list[connection[1]]
                ]),
                color = pg.mkColor((255, 0, 0)),
                width = 2,
                antialias = True
            ),
            FACE_CONNECTIONS
        ))
        self.face_line_list = list(filter(
            lambda x : x,
            self.face_line_list
        ))
        for item in self.face_line_list :
            if item :
                self.addItem(item)

    def updateWhole(self, landmark_list) :
        if "left_hand" in landmark_list :
            self.updateLeftHand(landmark_list["left_hand"])
        if "right_hand" in landmark_list :
            self.updateRightHand(landmark_list["right_hand"])
        if "pose" in landmark_list :
            pass
            self.updatePose(landmark_list["pose"])
        if "face" in landmark_list :
            pass
            #self.updateFace(landmark_list["face"])


if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)


    plot_widget = MediaPipeVisualizer()
    plot_widget.show()

    sys.exit(app.exec())


