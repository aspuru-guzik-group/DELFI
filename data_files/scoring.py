import re
import numpy as np

###########################################################################################
def main():
    
    def extract_energies_tdm(theolog):
        
        #open and read files
        with open(theolog, 'r') as f:
            log = f.readlines()
            
        # extract energies and fos from log file
        energies, tdm = [], []
        
        for state in range(2, len(log)):
            current_state = log[state].split()
            energies.append(float(current_state[1]))
            fos = float(current_state[2])
            mag = np.sqrt(((3/2)*fos/(float(current_state[1])))) 
            tdm.append(mag)
        
        
        return energies, tdm
    
###########################################################################################
    
    def extract_overlap(overlaplog):
        
        #open and read files
        with open(overlaplog, 'r') as f:
            log = f.readlines() 

        found_start=False
        matrixlines=[]
        for line in log:
            if found_start:
                matrixlines.append(line.strip())
            elif line.startswith('            |  1(1)a> '):
                found_start = True
                matrixlines.append(line.strip())


        ## extract the matrix from the output
        #findmatrixstring = "1(1)a> " + "(.*)"
        #regExprText  = re.findall(findmatrixstring, log, re.DOTALL | re.IGNORECASE)[0]
        #matrixlines= regExprText.rstrip().lstrip().splitlines()
        
        overlap = []

        for state in range(1, len(matrixlines)):
            ov_state = []
            current_state = matrixlines[state].split()
            for otherstate in range(2, len(current_state)):
                ov_state.append(abs(float(current_state[otherstate])))
            
            overlap.append(ov_state)
        
        return overlap
    
    
########################################################################################### 
    
    def calculate_score(nstates, overlap, dft_energies, dft_fos, adc_energies, adc_fos):
        
        score = 0
        try: 
            for state in range(nstates):
                diagonal = overlap[state][state]
            
                if diagonal >= 0.9:
                    ovlp_score = 1.0
                    consider_state = state
                elif diagonal < 0.9 and diagonal >= 0.5:
                    ovlp_score = diagonal
                    consider_state = state
                elif diagonal < 0.5 and diagonal >= 0.2:
                    if diagonal == max(overlap[state]):
                        ovlp_score = diagonal
                        consider_state = state
                    else:
                        biggest = max(overlap[state])
                        ovlp_score = biggest
                        consider_state = overlap[state].index(biggest)
                elif diagonal < 0.2:
                        biggest = max(overlap[state])
                        if biggest < 0.5:
                            state_score = 0.0
                        #print(state_score)
                            continue
                        elif biggest >= 0.90:
                            ovlp_score = 0.8
                            consider_state = overlap[state].index(biggest)
                        elif biggest < 0.90 and biggest >= 0.50:
                            ovlp_score = biggest
                            consider_state = overlap[state].index(biggest)
                energy_score = abs(adc_energies[consider_state]-dft_energies[consider_state])/2
                fos_score = abs(adc_fos[consider_state]-dft_fos[consider_state])/3
                    
                state_score = ovlp_score - energy_score - fos_score
                score += state_score
            
            #print(state_score)
        #print("\n")
        #print(score)
            if score < 0:
                final_score = 0
            else:
                final_score = round(score*20, 2) 
        except:
            final_score = "NaN"
        return final_score
    
    
########################################################################################### 

    dftenergies, dfttdm = extract_energies_tdm('tden_summ.txt')
    adcenergies, adcttdm = extract_energies_tdm('../ADC2/tdenadc2.txt')
    overlap = extract_overlap('overlap.txt')
    
    
    #print("TD-DFT energies: {}\n".format(dftenergies))
    #print("ADC energies: {}\n".format(adcenergies))
    #print("TD-DFT fos: {}\n".format(dftfos))
    #print("ADC fos: {}\n".format(adcfos))
    #print("overlap: {}\n".format(overlap))
    final_score = calculate_score(5, overlap, dftenergies, dfttdm, adcenergies, adcttdm)
    print(final_score)
    
#####################################################################################################

if __name__ == '__main__':
    main()
    
