import { Module } from '@nestjs/common';
import { UploadController } from './app.controller';
import { AppService } from './app.service';
import { FastifyMulterModule } from '@nest-lab/fastify-multer';

@Module({
  imports: [FastifyMulterModule],
  controllers: [UploadController],
  providers: [AppService],
})
export class AppModule {}
