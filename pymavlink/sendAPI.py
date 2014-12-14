def sendAPI(self, mavmsg, addr):
                '''send an API message'''
                buf = mavmsg.pack(self)
                self.file.Send(buf, addr)
                self.seq = (self.seq + 1) % 256
                self.total_packets_sent += 1
                self.total_bytes_sent += len(buf)
                if self.send_callback:
                    self.send_callback(mavmsg, *self.send_callback_args, **self.send_callback_kwargs)