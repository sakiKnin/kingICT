class Comparer:
   def compare(objectA, objectB):
      if objectA.originLocationCode==objectB.originLocationCode and objectA.destinationLocationCode==objectB.destinationLocationCode and objectA.departureDate==objectB.departureDate and objectA.adultNumber==objectB.adultNumber:
            return True
      return False
