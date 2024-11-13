# CTF Others Challenges | SecurityMaths | Writeup | Medium

SecurityMaths is a challenge that combines knowledge from mathematics, systems engineering and the analysis of GPS data. The idea is that GPS coordinates are divided into three parts and have to be put together. 

## Challenge Description
Prof. Schmidt’s coordinates to his favourite holiday destination were stolen. Unfortunately, he separated them into three pieces (due to security policies :p) which makes finding them quite difficult. However, the thief left some hints about their location. Now it's your turn to find them! 
- The student's favourite eating location.
- This place is quite interesting, but sadly, experiments are rather rare.
- That's a "SHAME"!

### Needed knowledge/tools
- Sine/Cosine rule (Maths)
- URI rule (SYT)
- Handling GPS coordinates (Determination of locations, evaluation, e.g. with Google Maps)

## Solution
1. **Find all pieces at their corresponding places**
   -  School cafeteria
   -  Physics laboratory
   -  Agreement with RAM
2. **Get the result of exercise one (system technology) with the help of URI (=x on the baseline)**
   - Calculate R3 \
     $R3=\frac{U3}{I3}$ \
     $R3=\frac{4.1125}{0.00876}=470\Omega$ 
   - Calculate Rges \
     $Rges=(\frac{R4 * R12}{R4 + R12})+180$ \
     $Rges=(\frac{470 * 320}{470 + 320})+180=370.38\Omega$ 
   - Calculate Iges \
     $Iges=\frac{Uges}{Rges}$ \
     $Iges=\frac{8}{370.38}=0.021599A=21.6mA$ 
> [!NOTE]
> This challenge may also be solved by using a simulation tool like [Tinkercad](https://www.tinkercad.com/).
> Only the digits before the comma are needed to get the unknown GPS part(=21)!
   
3. **Get the result of exercise two (math problem) with the help of sins/cosins rule (=y on the baseline)**
   - Calculate distance $\overline{AC}$ \
     $\overline{AC} = \sqrt{c^2 + d^2 - 2 * c * d * \cos(\gamma)}$ \
     $\overline{AC} = \sqrt{7^2 + 7.11^2 -2 * 7 * 7.11 * \cos(113)}=11.766cm$
   - Calculate $\beta$ \
     $\overline{AC}^2 = a^2 + b^2 - 2 * a * b * \cos(\beta)$ \
     $\beta = \arccos(\frac{a^2 + b^2 - \overline{AC}^2}{2 * a * b})$ \
     $\beta = \arccos(\frac{7^2 + 5^2 - 11.766^2}{2 * 7 * 5})=157.007°$
> [!NOTE]
> Only the digits before the comma are needed to get the unknown GPS part(=157)!

4. **Combine the results with the GPS coordinates baseline and determine the location behind them**
   - Can either be solved with [Google Maps](https://www.google.at/maps/) or [GPS-coordinates](https://www.gps-coordinates.net/).
   - Google Maps &rarr; Enter `21°18'50.0"N 157°51'18"W`
   - GPS-Coordinates &rarr; Enter the numbers in the corresponding boxes in the DMS section.
   - **Location:** Honolulu (Hawaii, USA) &rarr; `FF{Honolulu}`

> Keep in mind that the calculation part may already takes place after finding the corresponding piece. Furthermore, the places may variant due to adjustment to the challenge's description.

## Conclusion

SecurityMaths is a great opportunity to connect knowledge of various issues to end up having information that can be analysed further - in this case GPS coordinates that lead to Prof. Schmidt's favourite holiday destination.
