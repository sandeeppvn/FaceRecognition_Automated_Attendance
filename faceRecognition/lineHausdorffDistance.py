import numpy as np
import math
import copy

def penalty(angle):
	return angle**2;

def dist(x,y):
	return ((x[0]-y[0])**2 + (x[1]-y[1])**2)**(1/2)

def samePoint(x,y):
	if(x[0] == y[0] and x[1] == y[1]):
		return True
	return False

def closePoints(line1,line2):
	'''
	lis = [[dist(line1[0],line2[0]),line1[0],line2[0]],[dist(line1[1],line2[0]),line1[1],line2[0]],[dist(line1[0],line2[1]),line1[0],line2[1]],[dist(line1[1],line2[1]),line1[1],line2[1]]]
	lis.sort(key=lambda x: x[0])
	# print(lis)
	p1 = lis[0][1:]
	for i in lis[1:]:
		if(not samePoint(i[1],p1[0]) and not samePoint(i[2],p1[1])):
			p2 = i[1:]
	return [p1,p2]
	'''
	diff_x_1 = line1[0][0]-line1[1][0]
	diff_x_2 = line2[0][0]-line2[1][0]
	diff_y_1 = line1[0][1]-line1[1][1]
	diff_y_2 = line2[0][1]-line2[1][1]
	if((diff_y_1 > 0 and diff_y_2 > 0) or (diff_y_1 < 0 and diff_y_2 < 0)):
		p1 = line1[0],line2[0]
		p2 = line1[1],line2[1]
	elif((diff_y_1 > 0 and diff_y_2 < 0) or (diff_y_1 < 0 and diff_y_2 > 0)):
		p1 = line1[0],line2[1]
		p2 = line1[1],line2[0]
	else:
		if((diff_x_1 > 0 and diff_x_2 > 0) or (diff_x_1 < 0 and diff_x_2 < 0)):
			p1 = line1[0],line2[0]
			p2 = line1[1],line2[1]
		elif((diff_x_1 > 0 and diff_x_2 < 0) or (diff_x_1 < 0 and diff_x_2 > 0)):
			p1 = line1[0],line2[1]
			p2 = line1[1],line2[0]
		else:
			p1 = line1[0],line2[0]
			p2 = line1[1],line2[1]
	return p1,p2

def getSlope(x,y):
	if(not x):
		if(y>0) : 
			return math.pi/2
		else:
			return - math.pi/2
	else:
		return math.atan(y/x)

def getLength(line):
	return ((line[0][0]-line[1][0])**2+(line[0][1]-line[1][1])**2)**0.5

def positive(x):
	if(x < 0):
		return -x
	return x
def rotate(line1,line2,length,angle):
	if(angle == 0.0):
		return line1
	slope1 = getSlope(line1[1][0]-line1[0][0],line1[1][1] - line1[0][1])
	slope2 = getSlope(line2[1][0]-line2[0][0],line2[1][1] - line2[0][1])
	delta_x = (length/2) * math.sin(angle)
	delta_y = (length/2) * math.cos(angle)
	print("previous slope : ",math.degrees(slope1),math.degrees(slope2))
	if(slope1 < slope2):
		if(line1[0][0] - line1[1][0] < 0 or line1[0][1] - line1[1][1] < 0):
			line1[0][0] += delta_x
			line1[0][1] -= delta_y
			line1[1][0] -= delta_x
			line1[1][1] += delta_y
		else:
			line1[0][0] -= delta_x
			line1[0][1] += delta_y
			line1[1][0] += delta_x
			line1[1][1] -= delta_y
	elif(slope1 > slope2):
		if(line1[0][0] - line1[1][0] < 0 or line1[0][1] - line1[1][1] < 0):
			line1[0][0] -= delta_x
			line1[0][1] += delta_y
			line1[1][0] += delta_x
			line1[1][1] -= delta_y
		else:
			line1[0][0] += delta_x
			line1[0][1] -= delta_y
			line1[1][0] -= delta_x
			line1[1][1] += delta_y
	slope1 = getSlope(line1[1][0]-line1[0][0],line1[1][1] - line1[0][1])
	print("New slope : ",math.degrees(slope1),math.degrees(slope2),end="\n\n")			
	return line1

def findAngleDiff(line1,line2):
	slope1 = getSlope(line1[1][0]-line1[0][0],line1[1][1]-line1[0][1])
	slope2 = getSlope(line2[1][0]-line2[0][0],line2[1][1]-line2[0][1])
	angleDiff = slope2 - slope1
	return angleDiff


def LHD(line1,line2):
	# print(line1,line2)
	line1 = copy.deepcopy(line1)
	line2 = copy.deepcopy(line2)
	angleDiff = findAngleDiff(line1,line2)	
	vec1Len = getLength(line1)
	vec2Len = getLength(line2)
	if(vec1Len < vec2Len):
		line1 = rotate(line1, line2, vec1Len, angleDiff)
	else:
		line2 = rotate(line2, line1, vec2Len, -angleDiff)
	
	slope = getSlope(line1[1][0]-line1[0][0],line1[1][1] - line1[0][1]) + getSlope(line2[1][0]-line2[0][0],line2[1][1] - line2[0][1])
	slope /= 2
	points = closePoints(line1,line2)
	# print("Lines : ",line1,line2)
	# print("Points :",points)
	edgeSlopes = [getSlope(i[1][0]-i[0][0],i[1][1]-i[0][1]) for i in points]
	edgeAngle = [abs((math.pi/2)+slope-angle) if abs((math.pi/2)+slope-angle) <= (math.pi/2) else math.pi - abs((math.pi/2)+slope-angle) for angle in edgeSlopes]
	perDist = [dist(points[i][0],points[i][1])*math.cos(edgeAngle[i]) for i in range(len(points))]
	perDist = sum(perDist)/len(perDist)
	parDist = [dist(points[i][0],points[i][1])*math.sin(edgeAngle[i]) for i in range(len(points))]
	parDist = min(parDist)

	# print(line1,line2)
	return (penalty(angleDiff)**2 + perDist**2 + parDist**2 )**0.5
	# print(perDist)

def LHD_set_lines(lineSet1,lineSet2):
	totalLength = 0
	LHDSum = 0
	for line1 in lineSet1:
		line1Len = dist(line1[0],line1[1])
		totalLength += line1Len
		LHDSum += line1Len * min([LHD(line1,line2) for line2 in lineSet2])
	return LHDSum/totalLength

def primaryLHD(lineSet1,lineSet2):
	return max(LHD_set_lines(lineSet1,lineSet2),LHD_set_lines(lineSet2,lineSet1))


# print(LHD())
lineSet1 = [[[27, 110],[31, 129]],[[36, 147],[42, 165]],[[54, 179],[68, 192]],[[85, 202],[105, 203]],[[124, 200],[139, 188]],[[151, 173],[160, 157]],[[165, 138],[168, 119]],[[169, 100],[168, 80]]]
lineSet2 = [[[27, 111],[31, 130]],[[36, 147],[43, 163]],[[54, 178],[66, 191]],[[82, 201],[101, 203]],[[121, 201],[135, 189]],[[147, 173],[157, 156]],[[163, 138],[166, 119]],[[166, 100],[165, 81]]]
lineSet3 = [[[34, 125],[39, 144]],[[46, 161],[57, 177]],[[70, 191],[86, 201]],[[107, 202],[128, 201]],[[145, 192],[158, 178]],[[169, 161],[176, 143]],[[179, 123],[179, 103]]]
lineSet4 = [[[26, 92], [28, 110]], [[28, 110], [32, 127]], [[32, 127], [37, 144]], [[37, 144], [43, 161]], [[43, 161], [54, 176]], [[54, 176], [67, 186]], [[67, 186], [86, 196]], [[86, 196], [105, 197]], [[105, 197], [124, 194]], [[124, 194], [140, 185]], [[140, 185], [154, 174]], [[154, 174], [165, 158]], [[165, 158], [171, 138]], [[171, 138], [174, 119]], [[174, 119], [175, 98]], [[175, 98], [173, 79]]]
lineSet5 = [[[29, 81], [30, 100]], [[30, 100], [31, 119]], [[31, 119], [33, 139]], [[33, 139], [38, 158]], [[38, 158], [49, 175]], [[49, 175], [62, 190]], [[62, 190], [80, 202]], [[80, 202], [101, 204]], [[101, 204], [123, 202]], [[123, 202], [140, 190]], [[140, 190], [153, 175]], [[153, 175], [163, 159]], [[163, 159], [169, 140]], [[169, 140], [172, 120]], [[172, 120], [172, 100]], [[172, 100], [172, 81]]]
lineSet6 = [[[23, 75], [23, 97]], [[23, 97], [25, 118]], [[25, 118], [28, 138]], [[28, 138], [33, 158]], [[33, 158], [44, 177]], [[44, 177], [57, 192]], [[57, 192], [75, 203]], [[75, 203], [96, 204]], [[96, 204], [117, 202]], [[117, 202], [132, 191]], [[132, 191], [143, 176]], [[143, 176], [152, 160]], [[152, 160], [159, 141]], [[159, 141], [164, 123]], [[164, 123], [168, 103]], [[168, 103], [169, 82]]]

print(primaryLHD(copy.copy(lineSet1),copy.copy(lineSet1)))
print(primaryLHD(copy.copy(lineSet1),copy.copy(lineSet2)))
print(primaryLHD(copy.copy(lineSet1),copy.copy(lineSet3)))
# print(primaryLHD(copy.deepcopy(lineSet3),copy.deepcopy(lineSet3)))
# print(primaryLHD(copy.deepcopy(lineSet4),copy.deepcopy(lineSet4)))
# print(primaryLHD(copy.deepcopy(lineSet6),copy.deepcopy(lineSet6)))
