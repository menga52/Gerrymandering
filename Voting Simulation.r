electors = read.csv("~/Classes/CS/Gerrymandering/Gerrymandering/electoralVotes.csv")
trumpVotes = read.csv("~/Classes/CS/Gerrymandering/Gerrymandering/trump.csv")
bidenVotes = read.csv("~/Classes/CS/Gerrymandering/Gerrymandering/biden.csv")
stateSigmas = read.csv("~/Classes/CS/Gerrymandering/Gerrymandering/stateSigmas.csv")
men = 2
women = 3

g = function(state) {
  print(stateSigmas[state,3])
}

sims = function(n, reduction=0, pres=1, pop=0, winProp=0) {
  data = rep(0, n)
  for (i in 1:n) {
    data[i] = simElection(reduction, pres, pop)
  }
  if(pop==1) {
    if(winProp==1) {
      wins = 0
      for (i in 1:n) {
        if(data[i]>0.5) {
          wins = wins + 1
        }
      }
      return(wins/n)
    }
    else {
      return(mean(data))
    }
  }
  print(mean(data))
}

simElection = function(reduction, pres=1, pop=0) {
  # pop should be set to 1 only when pres=1
  trumpElectors = 0
  bidenElectors = 3 # forgot to include DC, but DC is super duper guaranteed blue
  bidenPop = 0
  repSenate = 0
  demSenate = 0
  stateOutcomes = rep(0, 50)
  for(state in 1:50) {
    sOutcome = simStateElection(state, reduction, pop)
    if(pop==1) {
      bidenPop = bidenPop + sOutcome*(electors[state, 2]-2)
    }
    if(simStateElection(state, reduction)==1) {
      stateOutcomes[state] = 1
      trumpElectors = trumpElectors + electors[state, 2]
      repSenate = repSenate + 2
    }
    else {
      bidenElectors = bidenElectors + electors[state, 2]
      demSenate = demSenate + 2
    }
  }
  if(pop==1) {
    return(bidenPop/538)
  }
  if(pres==0) {
    if(demSenate > repSenate) {
      return(1)
    }
    if(repSenate > demSenate) {
      return(0)
    }
    if(bidenElectors > trumpElectors) {
      return(1)
    }
    return(0)
  }
  if(bidenElectors>trumpElectors) {
    #print("biden win")
    return(1)
  }
  else if(trumpElectors>bidenElectors) {
    #print("trump win")
    return(0)
  }
  else {
    return(0)
  }
}

simStateManyTimes = function(state, reduction=0, reps=10000, sigma=-1) {
  total = 0
  for(i in 1:reps) {
    total = total + simStateElection(state, reduction, sigma=sigma)
  }
  return(total/reps)
}

simStateElection = function(state, reduction, popular=0, sigma=-1) {
  mProp = .59
  wProp = .63*(1 - reduction)
  total = mProp + wProp
  mProp = mProp/total
  wProp = wProp/total
  wTrumpMu = trumpVotes[state, women]
  mTrumpMu = trumpVotes[state, men]
  wBidenMu = bidenVotes[state, women]
  mBidenMu = bidenVotes[state, men]
  sigmaScaleFactor = stateSigmas[state, 2]
  if(sigma != -1) {
    #print(sigma)
    sigmaScaleFactor = sigma
  }
  wTrumpSigma = wTrumpMu*(1-wTrumpMu)*sigmaScaleFactor
  mTrumpSigma = mTrumpMu*(1-mTrumpMu)*sigmaScaleFactor
  wBidenSigma = wBidenMu*(1-wBidenMu)*sigmaScaleFactor
  mBidenSigma = mBidenMu*(1-mBidenMu)*sigmaScaleFactor
  wTrumpOutcome = rnorm(1, wTrumpMu, wTrumpSigma)
  mTrumpOutcome = rnorm(1, mTrumpMu, mTrumpSigma)
  wBidenOutcome = rnorm(1, wBidenMu, wBidenSigma)
  mBidenOutcome = rnorm(1, mBidenMu, mBidenSigma)
  trumpOutcome = wProp*wTrumpOutcome+mProp*mTrumpOutcome
  bidenOutcome = wProp*wBidenOutcome+mProp*mBidenOutcome
  if (popular==1) {
    total = trumpOutcome + bidenOutcome
    bidenOutcome = bidenOutcome / total
    return(bidenOutcome)
  }
  if (trumpOutcome>bidenOutcome) {
    return(1)
  }
  return(0)
}

sims2 = function(reps=10000) {
  bTotal = 0
  tTotal = 0
  for(i in 1:reps) {
    if(simHelper() == 1) {
      bTotal = bTotal + 1
    }
    else {
      tTotal = tTotal + 1
    }
  }
  print(bTotal/(bTotal+tTotal))
}

simHelper = function() {
  bTotal = 3 # Biden assumed to win DC
  tTotal = 0
  for(i in 1:50) {
    if(runif(1,0,1) > stateSigmas[i,5]) {
      bTotal = bTotal + electors[i,2]
    }
    else {
      tTotal = tTotal + electors[i,2]
    }
  }
  if(bTotal > tTotal) {
    return(1)
  }
  return(0)
}