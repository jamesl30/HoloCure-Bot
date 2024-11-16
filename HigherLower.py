#Note that counting cards does not work, Higher-Lower does not use the same deck of cards
#Also note that you never start with a King or an Ace, and that you will not be dealt the same card as you have
#I assume that all card types come with the same probabilities and maximize expected value of winnings
#Since averages are more affected by outliers, the expected winnings is higher than what you will usually win (the median)
def Expected_NoSwitch():
    #Calculating probability of winning a single round at all- used to calculate probability of winning next round if you choose to continue playing
    #Assumes there is no switches left
    #There are 132 total card combinations, and 96 of them will be won if choice with maximum expected value is chosen
    cnt = 0
    tot = 0
    for i in range(2, 13):
        cnt += max(i-1, 13-i)
        tot += 12
    return cnt / tot
def compute(mid):
    cur_prob = [1, 0] #odds of reaching current round
    ret = -1 #return of initial bet
    odds = [0, 0] #odds that we use the switch
    for i in range(2, 13):
        if max(i-1, 13-i) / 12 < mid:
            odds[0] += 1/12
        else:
            odds[1] += max(i-1, 13-i) / 12
    odds[1] /= 1 - odds[0]
    odds = [odds[0] * 96/132, odds[1]]
    for i in range(1, 5):
        cur_prob = [cur_prob[0] * odds[1], cur_prob[0] * odds[0] + cur_prob[1] * 96/132]
        ret += cur_prob[0] + cur_prob[1]
        if i != 1 and 96/132 < i / (i-1):
            cur_prob[1] = 0
        #TODO: implement break statement for including the hedge
    return ret
def Expected_Total():
    #binary search for optimal odds
    #Strategy: while prob of winning the next game is greater than the ratio of how much you will win to how much will be lost, move to the next round, otherwise cash out
    #If the current round being played has a probability of winning less than the optimal odds, we switch the cards
    prob = Expected_NoSwitch()
    low = 0
    high = 1
    while high - low > 0.0001:
        mid1 = low + (high - low) / 3
        mid2 = low + 2 * (high - low) / 3
        if compute(mid1) > compute(mid2):
            high = mid2
        else:
            low = mid1
    return low
print(Expected_Total())
#prints out 0.74, meaning that everything with odds >= 0.75 you should play with
