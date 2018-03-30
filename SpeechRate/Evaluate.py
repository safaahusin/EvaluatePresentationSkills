import Audio
import Filter
import Praat
import parselmouth

if __name__=="__main__":
    wordCount = 0
    minuteCount = 0
    totalWordsCount = 0

    print "Recording.........."
    while True:

        audio = Audio.Audio()
        WavFile = audio.audioRecord()
        filterNoisy = Filter.Filter()
        WavFilter = filterNoisy.low_filter(WavFile)
        snd = parselmouth.Sound(WavFilter)
        praatScript = Praat.Praat()
        words = praatScript.calcSyllbale(snd)
        wordCount += words
        totalWordsCount += words
        minuteCount += 1
        if minuteCount % 5 != 0:
            print "Words ", wordCount
            print "Minutes ", minuteCount

            if wordCount < 70:
                print "You're speaking too slow"
            elif wordCount >= 70 and wordCount < 100:  # maybe <105  or <120 it need more test
                print "Your speaking seem good"
            elif wordCount >= 100:
                print "You're speaking too fast"

            wordCount = 0
            print "Recording.........."
        else:
            break

    # When s/he Quit from This
    averageWords = totalWordsCount/minuteCount
    print "================================="
    print "Average Words ", averageWords
    print "Minutes ", minuteCount
    print "Final Evaluation : "
    if (averageWords < 70):
        print "\tYou're speaking slow"
    elif (averageWords >= 70 and averageWords < 100):  # maybe <105 it need more test
        print "\tYour speaking seem good"
    elif (averageWords >= 100):
        print "\tYou're speaking too fast"

