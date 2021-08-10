import sys
import numpy as np
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
import bezier
import math

class BezierCanvas(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.curves = []

    def add_curve(self,curve) -> bool:
        if(len(self.curves) > 0):
            last = self.curves[-1]
            x = last.nodes[0,-1]
            y = last.nodes[1,-1]
            if x != curve.nodes[0,0] or y != curve.nodes[1,0]:
                return False
            last,curve = self._smooth_curves(last,curve)
            self.curves[-1] = last
            print(self.curves[-1].nodes,curve.nodes)
            
        self.curves.append(curve)
        return True

    def _smooth_curves(self,c1,c2):
        first_nodes = c1.nodes
        last_nodes = c2.nodes
        p = first_nodes[:,-1]
        pre_p2 = first_nodes[:,-2]
        next_p1 = last_nodes[:,1]
        oa = pre_p2 - p
        ob = next_p1 - p
        oa_mag = math.sqrt(sum(i ** 2 for i in oa))
        ob_mag = math.sqrt(sum(i ** 2 for i in ob))
        oc = oa_mag * ob + ob_mag * oa
        print(oc)
        
        
        return c1,c2
        

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setPen(Qt.red)
        path = QPainterPath()
        if len(self.curves) <= 0:
            return
        w = self.width()
        h = self.height()
        path.moveTo(self.curves[0].nodes[0][0] * w , h - self.curves[0].nodes[1][0] * h)
        delta_t = 0.01
        for curve in self.curves:
            t = float(0)
            while(t < 1):
                p = curve.evaluate(t)
                path.lineTo(p[0][0] * w,h - p[1][0] * h)
                t += delta_t
        painter.drawPath(path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    canvas = BezierCanvas()
    nodes = np.asfortranarray([
        [0.0, 0.125, 0.3,0.4],
        [0.0, 0.2  , 0.3,0.7],
    ])
    curve = bezier.Curve.from_nodes(nodes)
    print(canvas.add_curve(curve))
    nodes = np.asfortranarray([
        [0.4,0.6,0.7,1.0],
        [0.7,0.4,0.2,0.1],
    ])
    curve = bezier.Curve.from_nodes(nodes)
    print(canvas.add_curve(curve))
    canvas.resize(400,300)
    canvas.show()
    sys.exit(app.exec_())

