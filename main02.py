from matrix import *


# main
docTermMat, tf_mat = dtm(1)
# print("term frequncy matrix ------------------------------ ")
# print(tf_mat[0,])

# print("DTM ------------------------------ ")
# print(docTermMat)

# print("TDM ------------------------------ ")
termDocMat = tdm(docTermMat)
# print(termDocMat)

# print("TDM ----first row -------------------------- ")
# print(termDocMat[0,])


# print("IDF ------------------------- ")
idf = idf(termDocMat, 1)
# print(idf)

# print("tf-idf ------------------------- ")
# print(tf_idf(tf_mat, idf))






