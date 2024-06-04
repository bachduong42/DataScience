import pandas as pd
import re
import unicodedata
data = pd.read_csv("../drawtable/testdatacrawl.csv")
data_lecturer = pd.read_csv("../crawdata/test_demo.csv")

cleandata = data.copy()
cleandata_lecturer = data_lecturer.copy()

# xóa các cột không cần thiết
cleandata.drop(columns=["id_categories", "id_cat_simple", "id_sub_category","id_course_category","id_course", "sub_category_name", "course_category_name"],axis=1,inplace=True)
cleandata_lecturer.drop(columns=['lecturer_id'], axis=1, inplace=True)
# cleandata_lecturer.drop(columns=["lecturer_id"],axis=1,inplace=True)
# đổi tên cột
rename_dict = {
    'category_name': 'Main_Category',
    'course_name': 'Course_Title',
    'headline': 'Description',
    'objectives_summary': 'Course_Content',
    'lecturers_name': 'Lecturers_name'
}
rename_dict_lecturer = {
    'lecturer_name': 'Name',
    'job_title': 'Job_Title',
    'category_name': 'Main_Category',
    'count': 'Count'
}

cleandata.rename(columns=rename_dict, inplace=True)
cleandata_lecturer.rename(columns=rename_dict_lecturer, inplace=True)

# loại bỏ các dữ liệu trùng lặp
cleandata.drop_duplicates(inplace=True)
cleandata_lecturer.drop_duplicates(inplace=True)

# loại bỏ các dữ liệu bị thiếu
cleandata.dropna(inplace=True)
cleandata_lecturer.dropna(inplace=True)

# phân chia câu trong Course Content
cleandata['Course_Content'] = cleandata['Course_Content'].str.replace('*', '. ')
cleandata['Lecturers_name'] = cleandata['Lecturers_name'].str.replace('*', '. ')
# loại bỏ các mẫu có văn bản không phải latinh
def has_non_latin(text):
    latin_pattern = re.compile(r'[^\x00-\x7F]+')
    return bool(re.search(latin_pattern, text))

non_latin_rows = cleandata.apply(lambda row: any(has_non_latin(str(value)) for value in row), axis=1)
non_latin_rows_lecturer = cleandata_lecturer.apply(lambda row: any(has_non_latin(str(value)) for value in row), axis=1)
# loại bỏ các hàng có ít nhất một ký tự không phải Latin
cleandata = cleandata[~non_latin_rows]
cleandata_lecturer = cleandata_lecturer[~non_latin_rows_lecturer]
# chuẩn hóa Unicode
def normalize_unicode(text):
    return unicodedata.normalize('NFC', text)
def normalize_unicode_in_dataframe(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(normalize_unicode)
    return df
data_normalized = normalize_unicode_in_dataframe(cleandata)
data_normalized_lecturer = normalize_unicode_in_dataframe(cleandata_lecturer)

# lưu file csv
cleandata.to_csv("CleanData.csv", index=False)
cleandata_lecturer.to_csv("CleanDataLecturer.csv", index=False)





