class Comparer:
   def compare(objA, objB):
      if objA.originLocationCode==objB.originLocationCode and objA.destinationLocationCode==objB.destinationLocationCode and objA.departureDate.strftime("%Y-%m-%d")==objB.departureDate and objA.adultNumber==int(objB.adultNumber):
            return True
      return False

