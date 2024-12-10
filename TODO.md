# TODOs

- [ ] Introduce a "maximum back-off", i.e. a minimum order (other than the 
  current hard-coded default of 1) down to which a back-off is performed. For 
  example, if the maximum back-off order is set to 2, and the lookup in the 
  2nd order MC does not yield a valid result, the word is terminated with a 
  `\n` immediately. This is to prevent too random letters form appearing.
- [ ] Use the `csv` library to load CSV data.
- [ ] Test whether using "starting characters" leads to better results. 
- [ ] Find a way to deal with non-letter chars, which can cause a bit of a 
  problem right now. For example, right now the common context `st.` as in 
  "St. Louis" can in principle be mistakenly used in the middle of a name:
  `August. Louis` would be a possible 3rd order result, which just doesn't 
  make sense linguistically. Using starting chars only prevents this for order
  four and above. Idea: limit prior to alphabetic characters only?