import curses
from curses.textpad import rectangle
import curses.ascii

def get_menu_choice( p_stdscr, p_choices_list, p_selected_int = 0 ) :
	# Clear the screen
	#p_stdscr.clear()
	# Get the size of the screen
	l_scr_size_yx = p_stdscr.getmaxyx()
	# Calculate half width and height
	l_center_yx = ( int( l_scr_size_yx[ 0 ] / 2 ), int( l_scr_size_yx[ 1 ] / 2 ) )
	# Find widest choice string
	l_widest_int = len( p_choices_list[ 'title' ] )

	# Set initial width of every column to 0
	l_col_width_list = [ 0 for x in range( len( p_choices_list[ 'choices' ][ 0 ] ) ) ]
	#l_col_width_list = [ 0 ] * len( p_choices_list[ 'choices' ][ 0 ] )
	# Go through all rows
	for choice_idx, choice_row in enumerate( p_choices_list[ 'choices' ] ):
		if len( str( choice_row[ 0 ] ) ) > l_widest_int : l_widest_int = len( str( choice_row[ 0 ] ) )
		# Go through all flield to find widest item per column
		for field_idx, field_value in enumerate( choice_row ) :
			l_width_int = len( str( field_value ) )
			if l_width_int > l_col_width_list[ field_idx ] :
				l_col_width_list[ field_idx ] = l_width_int

	# Start with an empty list
	l_concatenated_fields_list = []

	# Loop through all choice items, concatenate rows with multiple fields, find widest string
	for choice_idx, choice_row in enumerate( p_choices_list[ 'choices' ] ) :
		choice_itm_str = ''
		if len( choice_row ) > 1 :
			# Row contains multiple fields
			# Go through all fields
			for field_idx, field_value in enumerate( choice_row ) :
				if field_idx > 0 :
					choice_itm_str += '  ' + str( field_value ).ljust( l_col_width_list[ field_idx ] )
				else :
					choice_itm_str += str( field_value ).rjust( l_col_width_list[ field_idx ] )
			# Adjust widest width
			if len( choice_itm_str ) > l_widest_int : l_widest_int = len( choice_itm_str )
		elif len( choice_row ) == 1 :
			if len( str( choice_row[ 0 ] ) ) > l_widest_int : l_widest_int = len( str( choice_row[ 0 ] ) )

		# Center adjust single field row
		if len( choice_row ) == 1 :
			choice_itm_str += str( choice_row[ 0 ] ) #.center( l_widest_int )

		# Add padding
		l_padded_row_str = ' ' + choice_itm_str.center( l_widest_int ) + ' '
		# Add row to list
		l_concatenated_fields_list.append( l_padded_row_str )

	# Calculate half menu width and height
	l_menu_half_yx = ( int( len( p_choices_list ) / 2 ), int( l_widest_int / 2 ) )

	l_yx = ( l_center_yx[ 0 ] - l_menu_half_yx[ 0 ] - 2, l_center_yx[ 1 ] - l_menu_half_yx[ 1 ] )

	# Calculate uppler left corner coords
	l_ulyx = ( max( 1, l_yx[ 0 ] - 1 ), max( 1, l_yx[ 1 ] - 1 ) )
	# Calculate lower right corner coords
	l_lryx = (
		min( p_stdscr.getmaxyx()[ 0 ], l_yx[ 0 ] + 2 + len( p_choices_list[ 'choices' ] ) ),
		min( p_stdscr.getmaxyx()[ 1 ], l_yx[ 1 ] + 2 + l_widest_int )
	)

	l_newwin = p_stdscr.subwin(
		2 + len( p_choices_list[ 'choices' ] ),
		2 + l_widest_int,
		max( 1, l_yx[ 0 ] - 1 ),
		max( 1, l_yx[ 1 ] - 1 )
	)
	l_newwin.clear()
	del l_newwin
	rectangle( p_stdscr, l_ulyx[ 0 ], l_ulyx[ 1 ], l_lryx[ 0 ], l_lryx[ 1 ] )

	# Write the title
	p_stdscr.addstr( l_yx[ 0 ], l_yx[ 1 ], p_choices_list[ 'title' ].center( l_widest_int + 2 ) )

	# Stay in menu loop until user hits ENTER or ESC key
	l_user_key = -1
	while l_user_key not in [ curses.KEY_ENTER, 459, 13, 10, 27 ] :
		# Make sure selected index is within boundery
		if p_selected_int > len( p_choices_list[ 'choices' ] ) - 1 :
			p_selected_int = len( p_choices_list[ 'choices' ] ) - 1
		if p_selected_int < 0 : p_selected_int = 0
		# Display the menu choices
		for choice_idx, choice_row in enumerate( p_choices_list[ 'choices' ] ):
			l_yx = ( l_center_yx[ 0 ] - l_menu_half_yx[ 0 ] + choice_idx, l_center_yx[ 1 ] - l_menu_half_yx[ 1 ] )
			# Write row, with reversed colors if current row is selected
			if choice_idx == p_selected_int:
				p_stdscr.addstr( l_yx[ 0 ], l_yx[ 1 ], l_concatenated_fields_list[ choice_idx ], curses.A_REVERSE )
			else:
				p_stdscr.addstr( l_yx[ 0 ], l_yx[ 1 ], l_concatenated_fields_list[ choice_idx ] )

		# Get key from user
		l_user_key = p_stdscr.getch()
		# Change selected item depending on user input
		match l_user_key :
			case curses.KEY_UP   : p_selected_int -= 1
			case curses.KEY_DOWN : p_selected_int += 1
			case 27 :
				p_selected_int = -1
				break
	# Return choice id to caller
	return p_selected_int


def get_string_from_input( p_stdscr, p_msg_str, p_input_length_max_int = 1 ) :
	# Get the size of the screen
	l_scr_size_yx = p_stdscr.getmaxyx()
	l_scr_ctr_yx = ( int( l_scr_size_yx[ 0 ] / 2 ), int( l_scr_size_yx[ 1 ] / 2 ) )
	# Set limit of input string length
	p_input_length_max_int = min( p_input_length_max_int, l_scr_size_yx[ 1 ] )
	# Calculate half screen width and half screen height
	l_dlg_half_size_yx = ( max( 1, int( 3 / 2 ) ), int( ( 1 + len( p_msg_str ) + p_input_length_max_int + 1 ) / 2 ) )
	# Calculate border coords
	l_dlg_ulyx = ( max( 1, l_scr_ctr_yx[ 0 ] - l_dlg_half_size_yx[ 0 ] ), max( 1, l_scr_ctr_yx[ 1 ] - l_dlg_half_size_yx[ 1 ] ) )
	l_dlg_lryx = (
		min( l_scr_size_yx[ 0 ], l_scr_ctr_yx[ 0 ] + l_dlg_half_size_yx[ 0 ] ),
		min( l_scr_size_yx[ 1 ], l_scr_ctr_yx[ 1 ] + l_dlg_half_size_yx[ 1 ] )
	)

	# Draw a rectangle around the dialog window
	rectangle( p_stdscr, l_dlg_ulyx[ 0 ], l_dlg_ulyx[ 1 ], l_dlg_lryx[ 0 ], l_dlg_lryx[ 1 ] )
	p_stdscr.refresh()

	# Create a new window inside the dialog rectangle
	l_newwin = p_stdscr.subwin( l_dlg_lryx[ 0 ] - l_dlg_ulyx[ 0 ] , l_dlg_lryx[ 1 ] - l_dlg_ulyx[ 1 ], l_dlg_ulyx[ 0 ] + 1, l_dlg_ulyx[ 1 ] + 1 )
	l_newwin.refresh()

	# Write the dialog message
	l_newwin.addstr( 0, 0, p_msg_str )

	# Restore blinking cursor
	curses.curs_set( 1 )
	l_user_key = -1
	l_input_str = ''
	# Stay in menu loop until user hits ENTER key
	while l_user_key not in [ curses.KEY_ENTER, 459, 13, 10, 27 ] :
		# Get key from user
		l_user_key = l_newwin.getch( 0, len( p_msg_str ) + len( l_input_str ) )
		match l_user_key :
			case curses.KEY_BACKSPACE | 8 :
				# Erase last sharacter in the input string
				if len( l_input_str ) > 0 :
					# Slice the string, remove last char
					l_input_str = l_input_str[:len( l_input_str )-1 ]
					# write a space behind the shortened string
					l_newwin.addstr( 0, len( p_msg_str ) + len( l_input_str ), ' ' )
			case _ :
				# Limit the length of input string
				if len( l_input_str ) < p_input_length_max_int :
					# Add only visible chars
					if curses.ascii.isalnum( l_user_key ) or curses.ascii.isprint( l_user_key ):
						l_char = chr( l_user_key )
						l_input_str += l_char
		# Write the string to the screen
		l_newwin.addstr( 0, len( p_msg_str ), l_input_str )
		l_newwin.refresh()

	# Destroy the window dialog
	del l_newwin
	# Hide blinking cursor
	curses.curs_set( 0 )
	# Return string to caller
	return l_input_str
