import math
import csv
import googlemaps

#CSV FORMAT ZIPCODE = ZIPCODE,STATE,COUNTY,CITY,POPULATION,LATITUDE,LONGITUDE,HEALTHRISKSCORE

#provided files/key
ZIPCODEFILE = "ZIPCODES.csv"
HOSPITALFILE = "HOSP.csv"
API_KEY = 'KEYHERE'

#program generated files
DISTANCEMATRIXFILE = "DISTANCEMATRIX.csv"
DURATIONMATRIXFILE = "DURATIONMATRIX.csv"
BETAMATRIXFILE = "BETAMATRIX.csv"


class Zipcode():
    def __init__(self, zipcodeID): 
        self.zipcodeID = zipcodeID
        self.state = ""
        self.county = ""
        self.city = ""
        self.population = 0
        self.coordinates = (0.0, 0.0) #tuple of float
        self.populationRisk = 1
        return None

    #ADD/UPDATE DATA FUNCTIONS
    def addState(self, stateAbbrv):
        self.state = stateAbbrv
        return None
    
    def addCounty(self, countyName):
        self.county = countyName
        return None
    
    def addCity(self, cityName):
        self.city = cityName
        return None

    def addPopulation(self, peopleCount):
        self.population += peopleCount
        return None
    
    def updatePopulation(self, peopleCount):
        self.population = peopleCount
        return None
    
    def updateCoordinates(self, tupleCoordinates):
        self.coordinates = tupleCoordinates
        return None
    
    def updatePopulationRisk(self, riskScore):
        self.populationRisk = riskScore
        return None
    
    #DISPLAY DATA FUNCTIONS

    def displayZipcode(self):
        print("{" + str(self.zipcodeID) + ", " 
                  + str(self.state) + ", " 
                  + str(self.county) + ", " 
                  + str(self.city) + ", " 
                  + str(self.population) + ", "
                  + str(self.coordinates) + "}")
        return None



#CSV FORMAT HOSP = HNUM,COUNTY_NAME,LATITUDE,LONGTITUDE,HOSPITAL_NAME,BEDS,ZIPCODE,Hospital_Level_N_see_basis,Service_Level_Parameter_K_see_Basis

    
class Hospital():
    def __init__(self, hospitalID):
        self.hospitalID = hospitalID
        self.county = ""
        self.coordinates = (0.0, 0.0) #tuple of float
        self.name = ""
        self.bedCount = 0
        self.zipcode = ""
        self.serviceLevel_n = 0
        return None
    
    #ADD/UPDATE DATA FUNCTIONS
    def addCounty(self, countyName):
        self.county = countyName
        return None

    def updateCoordinates(self, tupleCoordinates): #lat, long
        self.coordinates = tupleCoordinates
        return None

    def addName(self, hospName):
        self.name = hospName
        return None

    def addBeds(self, totalBeds):
        self.bedCount += totalBeds
        return None
    
    def updateBeds(self, totalBeds):
        self.bedCount = totalBeds
        return None
    
    def updateZipcode(self, zipcodeID):
        self.zipcode = zipcodeID
        return None

    def serviceLevel(self, totalBeds):
    #https://www.ncbi.nlm.nih.gov/books/NBK333506/table/ch04.sec1.table1/
        n = 0
        if (totalBeds == 0 or totalBeds < 50):
            return 0
        elif (totalBeds >= 50 and totalBeds <= 250):
            n = 1
        elif (totalBeds > 250 and totalBeds <= 800):
            n = 2
        elif (totalBeds > 800 and totalBeds <= 1500):
            n = 3
        elif totalBeds > 1500:
            n = 4
        #print("n = " + str(n))
        k = (math.pow(2,(n-1)))
        self.serviceLevel_n = k
        return k
    
    #DISPLAY DATA FUNCTIONS

    def displayHospital(self):
        print("{" + str(self.hospitalID) + ", " 
                  + str(self.county) + ", " 
                  + str(self.coordinates) + ", " 
                  + str(self.name) + ", " 
                  + str(self.bedCount) + ", " 
                  + str(self.zipcode) + ", " 
                  + str(self.serviceLevel_n) + "}")
        return None



""" BLOCK CODE FOR USING TESTING OBJECTS

for each in hospitalObjList:
    each.displayHospital()

for each in zipcodeObjList:
    each.displayZipcode()

END BLOCK CODE FOR TESIING OBJECTS """

#SETTING = 'distance', 'duration''
#MODE = 'driving''

def createDistMatrix(apiKey, zipcodeObjectList, hospitalObjectList, FILENAME):
    gmaps = googlemaps.Client(apiKey)

    #file writing
    with open(FILENAME, 'w') as f:
        f.write("HID/ZIPCODE")
        f.write(",")

        #loop to write zipcode on first line
        for each_zObj in zipcodeObjectList:
            f.write(str(each_zObj.zipcodeID))
            f.write(",")
        
        f.write("\n")
        #loop end

        #loop to write Hospital Id and corresponding dist matrix between hID and zip
        for each_hObj in hospitalObjectList:
            hosp_coord = each_hObj.coordinates

            f.write(str(each_hObj.hospitalID))
            f.write(",")

            for each_zObj in zipcodeObjectList:
                zip_coord = each_zObj.coordinates

                #distance calc
                distance_m = gmaps.distance_matrix(hosp_coord, zip_coord, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]
                distance_km = distance_m / 1000

                #writing to file
                f.write(str(distance_km))
                f.write(",")
        
            f.write("\n")
    	#loop end
        
        f.close()
    #end loop

    return None


def createDurationMatrix(apiKey, zipcodeObjectList, hospitalObjectList, FILENAME):
    gmaps = googlemaps.Client(apiKey)

    #file writing
    with open(FILENAME, 'w') as f:
        f.write("HID/ZIPCODE")
        f.write(",")

        #loop to write zipcode on first line
        for each_zObj in zipcodeObjectList:
            f.write(str(each_zObj.zipcodeID))
            f.write(",")
        
        f.write("\n")
        #loop end

        #loop to write Hospital Id and corresponding dist matrix between hID and zip
        for each_hObj in hospitalObjectList:
            hosp_coord = each_hObj.coordinates

            f.write(str(each_hObj.hospitalID))
            f.write(",")

            for each_zObj in zipcodeObjectList:
                zip_coord = each_zObj.coordinates

                #distance calc
                time_s = gmaps.distance_matrix(hosp_coord, zip_coord, mode='driving')["rows"][0]["elements"][0]["duration"]["value"]
                time_m = time_s / 60

                #writing to file
                f.write(str(time_m))
                f.write(",")
        
            f.write("\n")
    	#loop end
        
        f.close()
    #end loop

    return None

#"3-0.04*'Precomputed Travel Time Matrix'!L5"
def createBetaMatrix(apiKey, zipcodeObjectList, hospitalObjectList, FILENAME):
    gmaps = googlemaps.Client(apiKey)

    #file writing
    with open(FILENAME, 'w') as f:
        f.write("HID/ZIPCODE")
        f.write(",")

        #loop to write zipcode on first line
        for each_zObj in zipcodeObjectList:
            f.write(str(each_zObj.zipcodeID))
            f.write(",")
        
        f.write("\n")
        #loop end

        #loop to write Hospital Id and corresponding dist matrix between hID and zip
        for each_hObj in hospitalObjectList:
            hosp_coord = each_hObj.coordinates

            f.write(str(each_hObj.hospitalID))
            f.write(",")

            for each_zObj in zipcodeObjectList:
                zip_coord = each_zObj.coordinates

                #distance calc
                time_s = gmaps.distance_matrix(hosp_coord, zip_coord, mode='driving')["rows"][0]["elements"][0]["duration"]["value"]
                time_m = time_s / 60
                beta = 3 - (0.04 * time_m)

                #writing to file
                f.write(str(beta))
                f.write(",")
        
            f.write("\n")
    	#loop end
        
        f.close()
    #end loop

    return None

    
    

#return distance/time matrix between zipcode id and Hospital id 
def returnMatrix(FILENAME, zipcodeObj, hospitalObj):
    with open(FILENAME) as distanceMatrixCSV:
        file_dist = csv.reader(distanceMatrixCSV, delimiter = ',') 
        line_count_zip = 0
        zipArr_count = 0
        zipLocated = 0
        #hospLocated = 0
        distance = 0

        for row_zip in file_dist:
            #first line is zipcode locations
            if line_count_zip == 0:
                #finding location of zipcode top row
                for each in row_zip:
                    if each == zipcodeObj.zipcodeID:
                        zipLocated = zipArr_count 
                    zipArr_count +=1

                line_count_zip += 1
            #next line find location of hospital in column
            else:
                #with both zipcode and hospital arrnum located
                if row_zip[0] == hospitalObj.hospitalID:
                    distance = row_zip[zipLocated]
                    #hospLocated = line_count_zip

                line_count_zip += 1
        
        distanceMatrixCSV.close()

    #print(distance)
    return float(distance)

""" BLOCK CODE FOR USING TESTING OBJECTS

print(returnMatrix(DISTANCEMATRIXFILE, zipcodeObjList[2], hospitalObjList[5]))
print(returnMatrix(DURATIONMATRIXFILE, zipcodeObjList[2], hospitalObjList[5]))
print(returnMatrix(BETAMATRIXFILE, zipcodeObjList[2], hospitalObjList[5]))


END BLOCK CODE FOR TESIING OBJECTS """

def huffSupply(zipcodeObject, hospitalObject):
    """#display for test purposes
    zipcodeObject.displayZipcode()
    hospitalObject.displayHospital()
    #end display"""

    #actual computation
    dist = returnMatrix(DISTANCEMATRIXFILE, zipcodeObject, hospitalObject)
    beta = returnMatrix(BETAMATRIXFILE, zipcodeObject, hospitalObject)
    distanceDecay = pow(dist, beta)
    supply_U = (hospitalObject.serviceLevel_n * hospitalObject.bedCount) / distanceDecay

    return supply_U


def huffDemand(zipcodeObjectList, hospitalObject):
    totalDemand = 0
    for zip in zipcodeObjectList:
        #distance decay calc
        dist = returnMatrix(DISTANCEMATRIXFILE, zip, hospitalObject)
        beta = returnMatrix(BETAMATRIXFILE, zip, hospitalObject)
        distanceDecay = pow(dist, beta)

        demand_V = (zip.populationRisk * zip.population) / distanceDecay

        totalDemand += demand_V

    
    return totalDemand

"""
for each_z in zipcodeObjList:
    for each_h in hospitalObjList:
        print(huffSupply(each_z, each_h))
    print("\n")
"""
"""
for each_h in hospitalObjList:
    print(huffDemand(zipcodeObjList, each_h))
"""
def huffAccessibility(zipcodeObject, zipcodeObjectList, hospitalObjectList):
    accessibilityTotal = 0
    for each_h in hospitalObjectList:
        #supply / demand
        supply = huffSupply(zipcodeObject, each_h)
        demand = huffDemand(zipcodeObjectList, each_h)
        accessibilityTotal += supply/demand

    return accessibilityTotal

def createAccessibilityFile(zipcodeObjectList, hospitalObjectList):
    with open('accessibilityscorematrix.txt', 'w') as f:
        f.write("ZIPCODE")
        f.write(",")
        f.write("ACCESSIBILITY SCORE")
        f.write("\n")

        for each_z in zipcodeObjectList:
            f.write(str(each_z.zipcodeID))
            f.write(",")
            f.write(str(huffAccessibility(each_z, zipcodeObjectList, hospitalObjectList)))
            f.write("\n")

        f.close()

    return None

def createNormalizedAccessibilityFile(zipcodeObjectList, hospitalObjectList):
    NORMALIZEDFACTOR = 10000
    with open('normalaccessibilityscorematrix.txt', 'w') as f:
        f.write("ZIPCODE")
        f.write(",")
        f.write("ACCESSIBILITY SCORE")
        f.write("\n")

        for each_z in zipcodeObjectList:
            f.write(str(each_z.zipcodeID))
            f.write(",")
            f.write(str(huffAccessibility(each_z, zipcodeObjectList, hospitalObjectList) * NORMALIZEDFACTOR))
            f.write("\n")

        f.close()

    return None

def main():
    #""" BLOCK CODE FOR USING TEST CSV in processing ZIPCODE objects
#CSV FORMAT ZIPCODE = ZIPCODE,STATE,COUNTY,CITY,POPULATION,LATITUDE,LONGITUDE,HEALTHRISKSCORE

    zipcodeObjList = []

    with open(ZIPCODEFILE) as zipcodeCsvFile:
        file_z = csv.reader(zipcodeCsvFile, delimiter = ',') 
        line_count_z = 0
        for row_z in file_z:
            if line_count_z == 0:
                line_count_z += 1
            else:
                tempZipObj = Zipcode(row_z[0])

                tempZipObj.addState(row_z[1])
                tempZipObj.addCounty(row_z[2])
                tempZipObj.addCity(row_z[3])
                tempZipObj.updatePopulation(int(row_z[4]))
                tempZipObj.updateCoordinates((float(row_z[5]), float(row_z[6])))
                #tempZipObj.updatePopulationRisk(float(row_z[7]))

                zipcodeObjList.append(tempZipObj)
                line_count_z += 1
        #print(f'Processed {line_count_z} lines.')

        zipcodeCsvFile.close()
        

    # END BLOCK CODE FOR USING TEST CSV in processing ZIPCODE objects """


    #""" BLOCK CODE FOR USING TEST CSV in processing HOSPITAL objects
    #CSV FORMAT HOSP = HNUM,COUNTY_NAME,LATITUDE,LONGTITUDE,HOSPITAL_NAME,BEDS,ZIPCODE

    hospitalObjList = []

    with open(HOSPITALFILE) as hospitalCsvFile:
        file_h = csv.reader(hospitalCsvFile, delimiter = ',') 
        line_count_h = 0
        for row_h in file_h:
            if line_count_h == 0:
                line_count_h += 1
            else:
                tempHospObj = Hospital(row_h[0])

                tempHospObj.addCounty(row_h[1])
                tempHospObj.updateCoordinates((float(row_h[2]), float(row_h[3])))
                tempHospObj.addName(row_h[4])
                tempHospObj.addBeds(int(row_h[5]))
                tempHospObj.updateZipcode(row_h[6])

                tempHospObj.serviceLevel(int(row_h[5]))

                hospitalObjList.append(tempHospObj)
                line_count_h += 1
        #print(f'Processed {line_count_h} lines.')

        hospitalCsvFile.close()

    # END BLOCK CODE FOR USING TEST CSV in processing HOSP objects """

    #MATRIX CREATION DURATIONMATRIX.csv
    #createDistMatrix(API_KEY, zipcodeObjList, hospitalObjList, DISTANCEMATRIXFILE)
    #createDurationMatrix(API_KEY, zipcodeObjList, hospitalObjList, DURATIONMATRIXFILE)
    #createBetaMatrix(API_KEY, zipcodeObjList, hospitalObjList, BETAMATRIXFILE)

    #ACCESSIBILITY CAL
    for each_z in zipcodeObjList:
        print(huffAccessibility(each_z, zipcodeObjList, hospitalObjList))
    
    createAccessibilityFile(zipcodeObjList, hospitalObjList)
    createNormalizedAccessibilityFile(zipcodeObjList, hospitalObjList)

if __name__ == '__main__':
    main()