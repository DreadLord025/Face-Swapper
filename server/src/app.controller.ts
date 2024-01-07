/* eslint-disable @typescript-eslint/no-var-requires */
import { File, FilesInterceptor } from '@nest-lab/fastify-multer';
import {
  Controller,
  Post,
  UseInterceptors,
  UploadedFiles,
  Res,
  BadRequestException,
} from '@nestjs/common';
import { exec } from 'child_process';
import { Response } from 'express';
import { promises as fs } from 'fs';
import { join } from 'path';
@Controller()
export class UploadController {
  @Post('upload')
  @UseInterceptors(FilesInterceptor('images'))
  async uploadImage(@UploadedFiles() files: Array<File>, @Res() res: Response) {
    if (!files || files.length === 0) {
      throw new BadRequestException('No files were uploaded.');
    }

    const uploadDir = join(__dirname, 'uploads');
    await fs.mkdir(uploadDir, { recursive: true });

    const image1Path = join(uploadDir, 'image1.jpg');
    const image2Path = join(uploadDir, 'image2.jpg');

    await fs.writeFile(image1Path, files[0].buffer);
    await fs.writeFile(image2Path, files[1].buffer);

    exec(
      `python ${'swapface.py'} ${image1Path} ${image2Path}`,
      { maxBuffer: 1024 * 1024 * 1024 },
      (error, stdout) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return;
        }

        // Разделяем stdout на две части
        const [img1_base64, img2_base64] = stdout.split('\n');

        res.send({
          img1: img1_base64,
          img2: img2_base64,
        });
      },
    );
  }
}
