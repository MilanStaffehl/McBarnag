# TODOs

- [ ] **Maximum back-off**: Introduce a "maximum back-off", i.e. a minimum order 
  (other than the current hard-coded default of 1) down to which a back-off is 
  performed. For example, if the maximum back-off order is set to 2, and the 
  lookup in the 2nd order MC does not yield a valid result, the word is 
  terminated with a `\n` immediately. This is to prevent too random letters 
  from appearing.
- [ ] **Limited prior**: limit prior to alphabetic characters only? This could prevent 
  random non-alphabetic characters from ruining the words.
- [ ] **Relative prior**: Change the meaning of `prior`: Large datasets should react the same 
  way to a prior of 0.02 as small datasets. Currently, however, a prior of 0.02
  means that there is a larger chance for random characters in small training
  datasets, but miniscule chances for large datasets. The prior should be set
  such that it is taken as a fraction of the total number of words in the 
  training data (i.e. for N words in the training data, a prior of 0.02 means
  that 0.02 * N is the prior for every character).
- [ ] **Start chars**: Test whether using "starting characters" leads to better 
  results. 
- [ ] Find a way to deal with non-letter chars, which can cause a bit of a 
  problem right now. For example, right now the common context `st.` as in 
  "St. Louis" can in principle be mistakenly used in the middle of a name:
  `August. Louis` would be a possible 3rd order result, which just doesn't 
  make sense linguistically. Using starting chars only prevents this for order
  four and above. 
- [x] Use the `csv` library to load CSV data.
