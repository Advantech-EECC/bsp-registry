#include <fcntl.h>
#include <iostream>
#include <linux/ptp_clock.h>
#include <linux/sockios.h>
#include <sys/ioctl.h>
#include <sys/time.h>
#include <unistd.h>
#include <cstring>
#include <time.h>

#ifndef CLOCKFD
#define CLOCKFD 3
#endif

#ifndef FD_TO_CLOCKID
#define FD_TO_CLOCKID(fd) ((~(clockid_t)(fd) << 3) | CLOCKFD)
#endif

// Function to open PTP device and return the file descriptor
int openPtpDevice(const std::string &device) {
    int fd = open(device.c_str(), O_RDWR);
    if (fd == -1) {
        perror("Failed to open PTP device");
        return -1;
    }
    return fd;
}

// Function to get the time from the PTP clock
void getPtpTime(int fd) {
    struct timespec ts;
    clockid_t clkid = FD_TO_CLOCKID(fd);
    if (clock_gettime(clkid, &ts) == -1) {
        perror("Failed to get PTP time");
        return;
    }

    std::cout << "PTP Clock Time: " 
              << ts.tv_sec << " seconds, " 
              << ts.tv_nsec << " nanoseconds" << std::endl;
}

// Function to adjust the PTP clock time
void adjustPtpTime(int fd, int64_t delta_sec, int32_t delta_nsec) {
    clockid_t clkid = FD_TO_CLOCKID(fd);
    struct timespec ts;

    // Get current time
    if (clock_gettime(clkid, &ts) == -1) {
        perror("Failed to get PTP time for adjustment");
        return;
    }

    // Add delta
    ts.tv_sec += delta_sec;
    ts.tv_nsec += delta_nsec;

    // Normalize
    if (ts.tv_nsec >= 1000000000) {
        ts.tv_sec++;
        ts.tv_nsec -= 1000000000;
    } else if (ts.tv_nsec < 0) {
        ts.tv_sec--;
        ts.tv_nsec += 1000000000;
    }

    // Set new time
    if (clock_settime(clkid, &ts) == -1) {
        perror("Failed to adjust PTP clock");
        return;
    }
    std::cout << "PTP Clock adjusted by " 
              << delta_sec << " sec and " 
              << delta_nsec << " nsec." << std::endl;
}

// Function to perform a time offset measurement
void measureTimeOffset(int fd) {
    struct ptp_extts_request req;
    memset(&req, 0, sizeof(req));

    req.index = 0;
    req.flags = PTP_ENABLE_FEATURE;

    if (ioctl(fd, PTP_ENABLE_PPS, &req) == -1) {
        perror("Failed to enable PPS");
        return;
    }

    std::cout << "PPS signal enabled for time offset measurement." << std::endl;
}

// Main function
int main(int argc, char *argv[]) {
    std::string device = "/dev/ptp0"; // Default PTP device

    if (argc > 1) {
        device = argv[1];
    } else {
        std::cout << "Usage: " << argv[0] << " [device_path]" << std::endl;
        std::cout << "Using default device: " << device << std::endl;
    }

    int ptpFd = openPtpDevice(device);
    if (ptpFd == -1) return 1;

    // Example: Get the PTP clock time
    getPtpTime(ptpFd);

    // Example: Adjust the PTP clock (e.g., add 10 seconds and 500 nanoseconds)
    adjustPtpTime(ptpFd, 10, 500);

    // Example: Measure time offset using PPS
    measureTimeOffset(ptpFd);

    // Close the PTP device
    close(ptpFd);

    return 0;
}