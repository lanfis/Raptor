#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <fcntl.h>
#include <termios.h>
#include <stdio.h>
#include <cstring>
#include <string>


class serial_handler
{
  private:
	struct termios oldio_;
	struct termios newio_;
	int fd_;
	bool is_open_ = false;
	const int buffer_size_ = 255;
	char buffer_[buffer_size_];
	
	string port_name_ = "/dev/ttyACM0";
	int baudrate_ = B57600;

	double tx_time_per_byte_ = 0;
	
  private:
//    void reset(){ bzero(&newio_, sizeof(newtio)); /* clear struct for new port settings */};
	bool setup_port();
	int get_cflag_baudrate(int baudrate);

  public:
	bool is_open(){ return is_open_; };
	void set_port(string port){ port_name_ = port;};
	string get_port(){return port_name_;};
	void set_baudrate(int baudrate){baudrate_ = baudrate;};
	int get_baudrate(){return baudrate_;};
	int read(string& packet){ int res = read(fd_, buffer_, buffer_size_); packet.assign(buffer_); return res; };
 /* read blocks program execution until a line terminating character is 
    input, even if more than 255 chars are input. If the number
    of characters read is smaller than the number of chars available,
    subsequent reads will return the remaining chars. res(return) will be set
    to the actual number of characters actually read 
*/
	int write(string& packet){ return write(fd_, packet.c_str(), packet.length()); };
	bool open(){ close(); fd_ = open(port_name_.c_str(), O_RDWR | O_NOCTTY | O_NONBLOCK); if(fd_ < 0) {is_open_ = false; return false;} is_open_ = true; return true; };
	bool open(string port_name, int baudrate){ set_port(port_name); set_baudrate(baudrate); return open(); };
	bool close(){ if(!is_open_) return false; close(fd_); is_open_ = false; return true;};
	void save_status(){ tcgetattr(fd, &oldio_); };
	void load_status(){ tcsetattr(fd, &newio_); };
	
	serial_handler();
	~serial_handler();
};

serial_handler::serial_handler()
{}

~serial_handler::serial_handler()
{}

double serial_handler::get_time()
{
	struct timespec tv;
	clock_gettime( CLOCK_REALTIME, &tv);
	return ((double)tv.tv_sec*1000.0 + (double)tv.tv_nsec*0.001*0.001);
}

bool serial_handler::setup_port()
{
	int clag_baud = get_cflag_baudrate(baudrate_);
	if(clag_baud == -1)
		return false;
	bzero(&newtio_, sizeof(newtio_)); // clear struct for new port settings
	newtio_.c_cflag = cflag_baud | CS8 | CLOCAL | CREAD | CRTSCTS;//8 data bits //	Local line - do not change "owner" of port //	Enable receiver
	newtio_.c_iflag = IGNPAR | ICRNL;//Ignore parity errors //Map CR to NL
	newtio_.c_oflag      = 0;
/*
  ICANON  : enable canonical input
  disable all echo functionality, and don't send signals to calling program
*/
	newtio_.c_lflag      = ICANON;
/* 
  initialize all control characters 
  default values can be found in /usr/include/termios.h, and are given
  in the comments, but we don't need them here
*/
	newtio.c_cc[VINTR]    = 0;     /* Ctrl-c */ 
	newtio.c_cc[VQUIT]    = 0;     /* Ctrl-\ */
	newtio.c_cc[VERASE]   = 0;     /* del */
	newtio.c_cc[VKILL]    = 0;     /* @ */
	newtio.c_cc[VEOF]     = 4;     /* Ctrl-d */
	newtio.c_cc[VTIME]    = 0;     /* inter-character timer unused */
	newtio.c_cc[VMIN]     = 1;     /* blocking read until 1 character arrives */
	newtio.c_cc[VSWTC]    = 0;     /* '\0' */
	newtio.c_cc[VSTART]   = 0;     /* Ctrl-q */ 
	newtio.c_cc[VSTOP]    = 0;     /* Ctrl-s */
	newtio.c_cc[VSUSP]    = 0;     /* Ctrl-z */
	newtio.c_cc[VEOL]     = 0;     /* '\0' */
	newtio.c_cc[VREPRINT] = 0;     /* Ctrl-r */
	newtio.c_cc[VDISCARD] = 0;     /* Ctrl-u */
	newtio.c_cc[VWERASE]  = 0;     /* Ctrl-w */
	newtio.c_cc[VLNEXT]   = 0;     /* Ctrl-v */
	newtio.c_cc[VEOL2]    = 0;     /* '\0' */

	// clean the buffer and activate the settings for the port
  	tcflush(fd_, TCIFLUSH);
	tcsetattr(fd_, TCSANOW, &newtio_);

	tx_time_per_byte = (1000.0 / (double)baudrate_) * 10.0;
	return true;
}

int serial_handler::get_cflag_baudrate(int baudrate)
{
	switch(baudrate)
	{
		case 9600:
			return B9600;
		case 19200:
      		return B19200;
		case 38400:
			return B38400;
		case 57600:
			return B57600;
		case 115200:
			return B115200;
		case 230400:
			return B230400;
		case 460800:
			return B460800;
		case 500000:
			return B500000;
		case 576000:
			return B576000;
		case 921600:
			return B921600;
		case 1000000:
			return B1000000;
		case 1152000:
			return B1152000;
		case 1500000:
			return B1500000;
		case 2000000:
			return B2000000;
		case 2500000:
			return B2500000;
		case 3000000:
			return B3000000;
		case 3500000:
			return B3500000;
		case 4000000:
			return B4000000;
		default:
			return -1;
	}
}
