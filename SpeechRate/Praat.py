import numpy as np

class Praat:

    def calcSyllbale(self, snd):
        # Process Step 1 --> Extract Intenstity
        intensity = snd.to_intensity(50, 0.016)
        # Process Step 2  --> take all peaks above certain threshold
        threshold = np.median(intensity.values)
        # print(Threshold)
        peaksThresh = filter(lambda x: x > threshold, intensity.values)

        # Process Step 3 -- > Inspect Dips and all Peaks from Intensity
        x = 1
        dips = []
        peaks = []
        dips.append(intensity.values[0])

        flag = True
        while x < len(intensity.values):
            if (intensity.values[x] > intensity.values[x - 1]) and not flag:
                dips.append(intensity.values[x - 1])
                flag = True
            elif (intensity.values[x] < intensity.values[x - 1]) and flag:
                peaks.append(intensity.values[x - 1])
                flag = False
            x += 1
        # Make length of dips and peaks equal
        if len(dips) < len(peaks):
            peaks.pop(len(peaks) - 1)
        elif len(peaks) < len(dips):
            dips.pop(len(dips) - 1)

        # Process Step 3 --> Preceding Dip with a peak of at least 2 DB
        peaksfilter = []
        i = 0
        while i < len(peaks):
            if (peaks[i] - dips[i]) >= 2 and peaks[i] in peaksThresh:
                peaksfilter.append(peaks[i])
            i += 1
        # print "From Step 3 This is Peaks Syllables : "
        # print peaksfilter

        # end Process 3

        # Process of Step 4 --> Pitch Contour and Extract Pitches
        pitch = snd.to_pitch(0.020, 50.0, 500.0)
        pitch_values = pitch.to_matrix().values

        j = 0
        listOfIndex = []
        while j < len(intensity.values):
            for peak in peaksfilter:
                if peak == intensity.values[j]:
                    if j >= len(pitch_values):
                        listOfIndex.append(len(pitch_values) - 1)
                    else:
                        listOfIndex.append(j)
            j += 1

        x = 0
        for index in listOfIndex:
            if pitch_values[index] == 0:
                peaksfilter.pop(x)
                x -= 1
            x += 1

        # print "From Step 4 This is Voiced Peaks Syllables :"
        # print peaksfilter
        syllables = len(peaksfilter)
        # print "Count of Syllables : ", Syllables

        words = int(round(syllables / 1.4))
        # print "Count of Words : ", Words

        return words
        # end Process
