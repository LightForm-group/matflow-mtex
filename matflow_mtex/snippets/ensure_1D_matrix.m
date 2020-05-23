function matrixVal = ensure_1D_matrix(matrixStr)
    if isa(matrixStr, 'double')
        matrixVal = matrixStr;
    else
        matrixVal = str2double(regexp(matrixStr, '(\d*[\.]*\d*)+', 'match'));
    end
end
