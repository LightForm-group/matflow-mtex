function cellArr = ensure_2D_cell_array(cellArrStr)
    cellArr = {};
    splitArr = split(cellArrStr, '} {');
    for i = 1:length(splitArr)   
        regMatch = regexp(splitArr{i}, '(-?\d*[\.]*\d*)+', 'match');
        disp(regMatch);
        cellArr{i} = num2cell(str2double(regMatch));
    end
end
