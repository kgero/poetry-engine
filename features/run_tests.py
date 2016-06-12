import tests.test_simple_count as test_simple_count
import tests.test_utils as test_utils
import simple_count, utils

if __name__ == '__main__':

	test_simple_count.test_num_words_in_line()
	test_simple_count.test_num_char_in_line()
	test_simple_count.test_num_letters_in_line()
	test_simple_count.test_num_stanzas_in_poem()
	test_simple_count.test_num_lines_in_poem()
	test_simple_count.test_num_words_in_poem()
	test_simple_count.test_num_char_in_poem()

	test_utils.test_get_poem()
	test_utils.test_get_lines()
	test_utils.test_get_words()
