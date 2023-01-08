import mediapipe as mp 
import cv2
import numpy as np
import time
from multiprocessing import Process
import sys
from playsound import playsound


cap = cv2.VideoCapture(0)

print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#cap = cv2.resize(cap, (320, 480), interpolation = cv2.INTER_AREA)


def func1():
	y = 0
	x = 0
	h = 320
	w = 480

	cPos = 0
	startT = 0
	endT = 0
	userSum = 0
	dur = 0
	isAlive = 1
	isInit = False
	cStart, cEnd = 0, 0
	isCinit = False
	tempSum = 0
	winner = 0
	inFrame = 0
	inFramecheck = False
	thresh = 180

	def calc_sum(landmarkList):

		tsum = 0
		for i in range(11, 33):
			tsum += (landmarkList[i].x * 480)

		return tsum

	def calc_dist(landmarkList):
		return (landmarkList[28].y * 640 - landmarkList[24].y * 640)

	def isVisible(landmarkList):
		if (landmarkList[28].visibility > 0.7) and (landmarkList[24].visibility > 0.7):
			return True
		return False

	mp_pose = mp.solutions.pose
	pose = mp_pose.Pose()
	drawing = mp.solutions.drawing_utils

	im1 = cv2.imread('im1.png')
	im2 = cv2.imread('im2.png')

	while(cap.isOpened()):
		ret, frame = cap.read()
		crop_image = frame[x:w, y:h]

		frame = crop_image


		frm = frame
		#_, frm = cap.read()
		rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
		res = pose.process(rgb)
		frm = cv2.blur(frm, (5, 5))
		drawing.draw_landmarks(frm, res.pose_landmarks, mp_pose.POSE_CONNECTIONS)

		if not (inFramecheck):
			try:
				if isVisible(res.pose_landmarks.landmark):
					inFrame = 1
					inFramecheck = True
				else:
					inFrame = 0
			except:
				print("You are not visible at all")

		if inFrame == 1:
			if not (isInit):
				print('\b')
				currWindow = im1
				startT = time.time()
				endT = startT
				dur = np.random.randint(1, 5)
				isInit = True

			if (endT - startT) <= dur:
				try:
					m = calc_dist(res.pose_landmarks.landmark)
					if m < thresh:
						cPos += 5

					print("current progress is : ", cPos)
				except:
					print("Not visible")

				endT = time.time()

			else:

				if cPos >= 100:
					print("WINNER")
					winner = 1

				else:
					if not (isCinit):
						isCinit = True
						cStart = time.time()
						cEnd = cStart
						currWindow = im2
						# playsound('redLight.mp3')
						userSum = calc_sum(res.pose_landmarks.landmark)

					if (cEnd - cStart) <= 3:
						tempSum = calc_sum(res.pose_landmarks.landmark)
						cEnd = time.time()
						if abs(tempSum - userSum) > 150:
							print("DEAD ", abs(tempSum - userSum))
							isAlive = 0

					else:
						isInit = False
						isCinit = False

			cv2.circle(currWindow, ((55 + 6 * cPos), 280), 15, (0, 0, 255), -1)

			mainWin = np.concatenate((cv2.resize(frm, (800, 400)), currWindow), axis=0)
			cv2.imshow("Main Window", mainWin)
		# cv2.imshow("window", frm)
		# cv2.imshow("light", currWindow)

		else:
			cv2.putText(frm, "Please Make sure you are fully in frame", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
						(0, 255, 0), 4)
			cv2.imshow("window", frm)

		if cv2.waitKey(1) == 27 or isAlive == 0 or winner == 1:
			cv2.destroyAllWindows()
			cap.release()
			break

func1()

