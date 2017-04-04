#! /usr/bin/env python3

from collections import namedtuple


def parse_course_listing_texts(filepath):
    course_nts = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if exclude_line(line):
            continue
        course_nts.append(build_namedtuple(line))

        if line:        # this finds the footer line (season & dept)
            season_dept = line.replace('\n', '')
    course_nts.pop()    # this remove the footer line from the main data list
    return course_nts, season_dept


def exclude_line(line):
    if not line.strip():
        return True
    for exclude in ("CROSS-LISTED", "----------", "ENRL", "BEGIN-END"):
        if exclude in line:
            return True
    return False


CourseItem = namedtuple("CourseItem", ["available", "enrollment_count", "abbr_num", "type", "sec_num",
                                       "course_title", "credit_hours", "begin_end", "days", "room",
                                       "building", "special_enrollment", "instructor"])


def build_namedtuple(line):
    # the printout of the courses follows a patter of splitting elements at predetermined widths
    return CourseItem(line[:4].strip(), line[4:10].strip(), line[10:21].strip(), line[21:28].strip(), line[28:31].strip(),
                      line[31:55].strip(), line[55:59].strip(), line[59:70].strip(), line[70:79].strip(), line[79:84].strip(),
                      line[85:99].strip(), line[100:117].strip(), line[117:].strip())


if __name__ == '__main__':
    courseNT_seasonDept = parse_course_listing_texts('filepath_to_scraped_course.txt')
