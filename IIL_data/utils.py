def give_questions(tag, usecase):

  keyword1 = tag
  keyword2 = usecase

  questions = [
      """All information related to """ +  keyword1 + """ in """ +  keyword2 + 
      """ for service and maintenance along with cause for anomaly """,
      "Give me a taxonomy for " +  keyword2 ,
      "All information about the " + keyword1 + " in " +  keyword2 ,
      "Role of " +  keyword1 + " in anomaly for " +  keyword2  ,
      " Root Cause for " + keyword1 + " as anomaly in "  +  keyword2 ,
      "Recommendation for Solution for " + keyword1 +  " related anomaly in "  +  keyword2 ,
      " Preventive Action for " + keyword1 + " related anomaly in " + keyword2 ,
      " Corrective Action for " + keyword1 + " related anomaly in " + keyword2 
  ]
  
  return questions